from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from cloudinary.models import CloudinaryField

User = get_user_model()

# LISTING TYPE CHOICES
LISTING_TYPE_CHOICES = [
    ('full', 'Full Apartment/House'),
    ('room', 'Single Room'),
]

POSTING_TYPE_CHOICES = [
    ('offering', 'I am offering a sublet'),
    ('seeking', 'I am seeking a sublet'),
]

# SEMESTER/DURATION CHOICES
DURATION_CHOICES = [
    ('fall', 'Fall Semester'),
    ('spring', 'Spring Semester'),
    ('summer', 'Summer'),
    ('winter_break', 'Winter Break'),
    ('spring_break', 'Spring Break'),
    ('thanksgiving', 'Thanksgiving Break'),
    ('full_year', 'Full Academic Year'),
    ('custom', 'Custom Dates'),
]

# ROOMMATE PREFERENCES
ROOMMATE_GENDER_CHOICES = [
    ('any', 'Any'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('non_binary', 'Non-Binary'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('rented', 'Rented'),
]

class Campus(models.Model):
    school_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Campuses"
    
    def __str__(self):
        return f"{self.school_name} - {self.city}, {self.state}"

class Listing(models.Model):
    # Basic Info
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # NEW: Posting type
    posting_type = models.CharField(max_length=20, choices=POSTING_TYPE_CHOICES, default='offering')
    
    # Listing Type
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='full')
    
    # Price
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Property Details
    beds = models.IntegerField()
    baths = models.DecimalField(max_digits=3, decimal_places=1)
    
    # Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # APARTMENT AMENITIES
    furnished = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    washer_dryer_in_unit = models.BooleanField(default=False)
    dishwasher = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    
    # BUILDING AMENITIES
    gym = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    parking_spaces = models.IntegerField(null=True, blank=True, help_text="Number of parking spaces")
    doorman = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    laundry_in_building = models.BooleanField(default=False)
    bike_storage = models.BooleanField(default=False)
    
    # UTILITIES (Individual toggles)
    electricity_included = models.BooleanField(default=False)
    water_included = models.BooleanField(default=False)
    gas_included = models.BooleanField(default=False)
    internet_included = models.BooleanField(default=False)
    cable_included = models.BooleanField(default=False)
    
    # ROOMMATE INFO (for rooms)
    has_roommates = models.BooleanField(default=False)
    number_of_roommates = models.IntegerField(null=True, blank=True)
    roommate_gender = models.CharField(max_length=20, choices=ROOMMATE_GENDER_CHOICES, default='any', blank=True)
    
    # LEASE DETAILS
    duration_type = models.CharField(max_length=20, choices=DURATION_CHOICES, default='custom')
    lease_start = models.DateField()
    lease_end = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Boosting
    is_boosted = models.BooleanField(default=False)
    boosted_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_bumped = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-is_boosted', '-last_bumped', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_price_color(self):
        # Price affordability indicator
        if self.rent < 1000:
            return 'success'
        elif self.rent < 2000:
            return 'warning'
        else:
            return 'danger'
    
    def bump(self):
        self.last_bumped = timezone.now()
        self.save()

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'order']
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ListingImage.objects.filter(listing=self.listing, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'listing')

class ContactMessage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
