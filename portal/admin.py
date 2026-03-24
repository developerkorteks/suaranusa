from django.contrib import admin
from .models import AdSlot

@admin.register(AdSlot)
class AdSlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'position_slug', 'is_active', 'updated_at')
    list_filter = ('is_active', 'position_slug')
    search_fields = ('name', 'position_slug')
    ordering = ('position_slug',)
    
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'position_slug', 'is_active')
        }),
        ('Scripts & Links (Adsterra)', {
            'description': 'Paste the raw JS code for standard ads OR the destination URL for Smartlinks.',
            'fields': ('desktop_script', 'mobile_script', 'direct_url')
        }),
    )
