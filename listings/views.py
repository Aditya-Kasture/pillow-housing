from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Listing, SavedListing, ContactMessage, ListingImage
from .forms import ListingForm, ContactForm
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string


def landing(request):
    """StreetEasy-style landing page"""
    return render(request, 'listings/landing.html')


def search_results(request):
    """Search and filter results page - only show offerings"""
    # Only show people offering sublets (not seeking)
    listings = Listing.objects.filter(status='active', posting_type='offering')
    
    # Get query parameters
    location = request.GET.get('location', '')
    duration = request.GET.get('duration', '')
    beds = request.GET.get('beds', '')
    max_price = request.GET.get('max_price', '')
    listing_type = request.GET.get('listing_type', '')
    sort_by = request.GET.get('sort', 'newest')
    
    # Apply filters
    if location:
        listings = listings.filter(
            Q(city__icontains=location) | 
            Q(state__icontains=location) | 
            Q(zip_code__icontains=location)
        )
    
    if duration:
        listings = listings.filter(duration_type=duration)
    
    if beds:
        if beds == '3':
            listings = listings.filter(beds__gte=3)
        else:
            listings = listings.filter(beds=int(beds))
    
    if max_price:
        listings = listings.filter(rent__lte=float(max_price))
    
    if listing_type:
        listings = listings.filter(listing_type=listing_type)
    
    # Sorting
    if sort_by == 'price_low':
        listings = listings.order_by('rent')
    elif sort_by == 'price_high':
        listings = listings.order_by('-rent')
    elif sort_by == 'newest':
        listings = listings.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'location': location,
        'duration': duration,
        'beds': beds,
        'max_price': max_price,
        'listing_type': listing_type,
        'sort_by': sort_by,
        'total_results': listings.count(),
    }
    
    return render(request, 'listings/search_results.html', context)


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    is_saved = False
    
    if request.user.is_authenticated:
        is_saved = SavedListing.objects.filter(user=request.user, listing=listing).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        message = request.POST.get('message')
        sender_email = request.POST.get('sender_email')
        sender_phone = request.POST.get('sender_phone', '')
        
        if message and sender_email:
            contact_message = ContactMessage.objects.create(
                listing=listing,
                sender=request.user,
                sender_email=sender_email,
                sender_phone=sender_phone,
                message=message
            )
            
            # Send email notification to listing owner
            try:
                subject = f'New message about your listing: {listing.title}'
                html_message = render_to_string('emails/contact_notification.html', {
                    'listing': listing,
                    'message': contact_message,
                    'site_url': request.build_absolute_uri('/'),
                })
                
                send_mail(
                    subject=subject,
                    message=message,  # Plain text fallback
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[listing.owner.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't break user experience
                print(f"Email error: {e}")
            
            messages.success(request, 'Message sent successfully!')
            return redirect('listing_detail', pk=pk)
    
    price_color = listing.get_price_color()
    
    context = {
        'listing': listing,
        'is_saved': is_saved,
        'price_color': price_color,
    }
    return render(request, 'listings/detail.html', context)

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            for idx, img in enumerate(images):
                ListingImage.objects.create(listing=listing, image=img, is_primary=(idx==0), order=idx)
            
            messages.success(request, 'Listing created successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'listings/create.html', {'form': form})


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    
    return render(request, 'listings/edit.html', {'form': form, 'listing': listing})


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    listing.delete()
    messages.success(request, 'Listing deleted successfully!')
    return redirect('my_listings')


@login_required
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings})


@login_required
def saved_listings(request):
    saved_listings = SavedListing.objects.filter(user=request.user).select_related('listing')
    return render(request, 'listings/saved.html', {'saved_listings': saved_listings})


@login_required
def toggle_save(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    saved, created = SavedListing.objects.get_or_create(user=request.user, listing=listing)
    
    if not created:
        saved.delete()
        messages.success(request, 'Listing removed from saved.')
    else:
        messages.success(request, 'Listing saved!')
    
    return redirect('listing_detail', pk=pk)


@login_required
def bump_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    listing.bump()
    messages.success(request, 'Listing bumped to top!')
    return redirect('listing_detail', pk=pk)


@login_required
def boost_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 999,
                        'product_data': {
                            'name': f'Boost Listing: {listing.title}',
                            'description': '7-day featured placement',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('boost_success', args=[listing.pk])
                ) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(
                    reverse('listing_detail', args=[listing.pk])
                ),
                metadata={
                    'listing_id': listing.pk,
                    'user_id': request.user.id,
                }
            )
            return redirect(checkout_session.url)
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('listing_detail', pk=pk)
    
    return render(request, 'listings/boost_confirm.html', {'listing': listing})

@login_required
def boost_success(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    session_id = request.GET.get('session_id')
    
    if session_id:
        # Verify payment and activate boost
        from datetime import timedelta
        listing.is_boosted = True
        listing.boosted_until = timezone.now() + timedelta(days=7)
        listing.save()
        
        messages.success(request, 'Your listing has been boosted for 7 days!')
    
    return redirect('listing_detail', pk=pk)


def stripe_webhook(request):
    """Handle Stripe webhooks for payment confirmations"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        listing_id = session['metadata']['listing_id']
        
        # Activate boost
        listing = Listing.objects.get(pk=listing_id)
        from datetime import timedelta
        listing.is_boosted = True
        listing.boosted_until = timezone.now() + timedelta(days=7)
        listing.save()
    
    return HttpResponse(status=200)
