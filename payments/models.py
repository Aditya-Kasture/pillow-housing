from django.db import models
from django.conf import settings
from listings.models import Listing

class BoostPayment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='boost_payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_checkout_session_id = models.CharField(max_length=200, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Boost for {self.listing.title}"
