from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import AdSlot, ManualArticle

@admin.register(ManualArticle)
class ManualArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'author', 'publish_date', 'is_published')
    list_filter = ('category', 'is_published', 'publish_date')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    ordering = ('-publish_date',)

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
