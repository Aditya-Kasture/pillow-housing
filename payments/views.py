from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import stripe

from listings.models import Listing
from .models import BoostPayment

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def boost_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    messages.info(request, 'Stripe integration coming soon!')
    return redirect('listing_detail', pk=pk)

def boost_success(request):
    messages.success(request, 'Boost successful!')
    return redirect('home')

@csrf_exempt
def stripe_webhook(request):
    return HttpResponse(status=200)
