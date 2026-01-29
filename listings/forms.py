from django import forms
from .models import Listing, ContactMessage

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'posting_type', 'listing_type', 'title', 'description', 'rent', 
            'beds', 'baths', 'address', 'city', 'state', 'zip_code',
            
            # Apartment Amenities
            'furnished', 'pets_allowed', 'washer_dryer_in_unit', 'dishwasher',
            'air_conditioning', 'heating', 'balcony',
            
            # Building Amenities
            'gym', 'pool', 'parking', 'parking_spaces', 'doorman', 
            'elevator', 'laundry_in_building', 'bike_storage',
            
            # Utilities
            'electricity_included', 'water_included', 'gas_included',
            'internet_included', 'cable_included',
            
            # Roommate Info
            'has_roommates', 'number_of_roommates', 'roommate_gender',
            
            # Lease
            'duration_type', 'lease_start', 'lease_end'
        ]
        widgets = {
            'posting_type': forms.Select(attrs={'class': 'form-select'}),
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'rent': forms.NumberInput(attrs={'class': 'form-control'}),
            'beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'baths': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_type': forms.Select(attrs={'class': 'form-select'}),
            'lease_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lease_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_roommates': forms.NumberInput(attrs={'class': 'form-control'}),
            'roommate_gender': forms.Select(attrs={'class': 'form-select'}),
            'parking_spaces': forms.NumberInput(attrs={'class': 'form-control'}),
            'furnished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pets_allowed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'washer_dryer_in_unit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dishwasher': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'air_conditioning': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'heating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gym': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doorman': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'elevator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'laundry_in_building': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bike_storage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'electricity_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'water_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gas_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'internet_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cable_included': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_roommates': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['message', 'sender_email', 'sender_phone']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sender_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
