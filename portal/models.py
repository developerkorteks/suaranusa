from django.db import models
from django.core.cache import cache

class AdSlot(models.Model):
    """
    Dynamic Advertisement Slot Management for suaranusa.
    Allows easy Adsterra integration via Django Admin.
    """
    SLOT_POSITIONS = [
        ('popunder', 'Global Popunder (Head)'),
        ('social_bar', 'Global Social Bar (Footer)'),
        ('top_leaderboard', 'Top Banner (Below Navbar)'),
        ('sidebar_modular', 'Sidebar Banner (Right Column)'),
        ('mid_article', 'Mid-Article Banner (Inside Content)'),
        ('footer_banner', 'Bottom Banner (Footer Area)'),
        ('smartlink_general', 'Smartlink URL (For buttons/links)'),
    ]

    name = models.CharField(max_length=100, help_text="Internal name for identification (e.g. 'Home Top Banner')")
    position_slug = models.CharField(
        max_length=50, 
        choices=SLOT_POSITIONS, 
        unique=True,
        help_text="Unique position identifier used in templates"
    )
    desktop_script = models.TextField(blank=True, null=True, help_text="Paste Adsterra Desktop JS code here")
    mobile_script = models.TextField(blank=True, null=True, help_text="Paste Adsterra Mobile JS code here")
    direct_url = models.URLField(blank=True, null=True, help_text="For Smartlinks: Paste the direct destination URL here")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.repopulate_cache()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.repopulate_cache()

    def repopulate_cache(self):
        # Local import to avoid circular dependencies
        from django.core.cache import cache
        active_slots = AdSlot.objects.filter(is_active=True)
        data = []
        for slot in active_slots:
            data.append({
                'slug': slot.position_slug,
                'm_script': slot.mobile_script,
                'd_script': slot.desktop_script,
                'd_url': slot.direct_url
            })
        cache.set('active_ad_slots_data', data, None)

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} [{self.position_slug}] - {status}"

    class Meta:
        verbose_name = "Advertisement Slot"
        verbose_name_plural = "Advertisement Slots"
