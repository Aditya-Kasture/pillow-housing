from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('search/', views.search_results, name='search_results'),
    path('listings/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listings/create/', views.create_listing, name='create_listing'),
    path('listings/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('listings/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('listings/<int:pk>/bump/', views.bump_listing, name='bump_listing'),
    path('listings/<int:pk>/boost/', views.boost_listing, name='boost_listing'),
    path('listings/<int:pk>/boost/success/', views.boost_success, name='boost_success'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('saved/', views.saved_listings, name='saved_listings'),
    path('listings/<int:pk>/toggle-save/', views.toggle_save, name='toggle_save'),
    
    # Messaging System
    path('listings/<int:pk>/message/', views.send_message, name='send_message'),
    path('listings/<int:pk>/inquiry/', views.inquiry_form, name='inquiry_form'),
    path('inbox/', views.inbox, name='inbox'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
]
