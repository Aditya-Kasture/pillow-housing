from django.contrib import admin
from .models import Listing, ListingImage, SavedListing, ContactMessage, Campus

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'city', 'state', 'rent', 'listing_type', 'duration_type', 'status', 'is_boosted', 'created_at']
    list_filter = ['status', 'listing_type', 'duration_type', 'posting_type', 'is_boosted', 'created_at']
    search_fields = ['title', 'description', 'city', 'state', 'address']
    inlines = [ListingImageInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('owner', 'posting_type', 'listing_type', 'title', 'description', 'status')
        }),
        ('Pricing & Details', {
            'fields': ('rent', 'beds', 'baths')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
        ('Lease Details', {
            'fields': ('duration_type', 'lease_start', 'lease_end')
        }),
        ('Apartment Amenities', {
            'fields': ('furnished', 'pets_allowed', 'washer_dryer_in_unit', 'dishwasher', 
                      'air_conditioning', 'heating', 'balcony'),
            'classes': ('collapse',)
        }),
        ('Building Amenities', {
            'fields': ('gym', 'pool', 'parking', 'parking_spaces', 'doorman', 
                      'elevator', 'laundry_in_building', 'bike_storage'),
            'classes': ('collapse',)
        }),
        ('Utilities', {
            'fields': ('electricity_included', 'water_included', 'gas_included', 
                      'internet_included', 'cable_included'),
            'classes': ('collapse',)
        }),
        ('Roommate Info', {
            'fields': ('has_roommates', 'number_of_roommates', 'roommate_gender'),
            'classes': ('collapse',)
        }),
        ('Boosting', {
            'fields': ('is_boosted', 'boosted_until', 'last_bumped')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'is_primary', 'order', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']

@admin.register(SavedListing)
class SavedListingAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'listing__title']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'sender', 'sender_email', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'sender_email', 'message']
    readonly_fields = ['created_at']

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'city', 'state']
    search_fields = ['school_name', 'city', 'state']
