from django.core.management.base import BaseCommand
from django.core.cache import cache
from portal.models import AdSlot

class Command(BaseCommand):
    help = 'Populate the advertisement cache from the database'

    def handle(self, *args, **options):
        active_slots = AdSlot.objects.filter(is_active=True)
        data = []
        for slot in active_slots:
            data.append({
                'slug': slot.position_slug,
                'm_script': slot.mobile_script,
                'd_script': slot.desktop_script,
                'd_url': slot.direct_url
            })
        
        # Set cache without expiration (or set a long one)
        cache.set('active_ad_slots_data', data, None)
        self.stdout.write(self.style.SUCCESS(f'Successfully cached {len(data)} ad slots'))
