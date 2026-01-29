from django.urls import path
from . import views

urlpatterns = [
    path('boost/<int:pk>/', views.boost_listing, name='boost_listing'),
    path('boost/success/', views.boost_success, name='boost_success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
