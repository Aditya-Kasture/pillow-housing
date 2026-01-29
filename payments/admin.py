from django.contrib import admin
from .models import BoostPayment

@admin.register(BoostPayment)
class BoostPaymentAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'amount', 'status', 'created_at']
    list_filter = ['status']
