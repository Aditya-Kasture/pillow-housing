from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from listings.models import Listing

class Command(BaseCommand):
    help = 'Auto-pause listings that have not been bumped in 7 days'

    def handle(self, *args, **kwargs):
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        # Find active listings that haven't been bumped in 7 days
        stale_listings = Listing.objects.filter(
            status='active',
            last_bumped__lt=seven_days_ago
        ) | Listing.objects.filter(
            status='active',
            last_bumped__isnull=True,
            created_at__lt=seven_days_ago
        )
        
        count = stale_listings.count()
        stale_listings.update(status='pending')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully paused {count} stale listings')
        )
