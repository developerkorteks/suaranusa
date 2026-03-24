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
        # Clear ad caches on any change
        cache.delete('active_ad_slots_mobile')
        cache.delete('active_ad_slots_desktop')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete('active_ad_slots_mobile')
        cache.delete('active_ad_slots_desktop')
        super().delete(*args, **kwargs)

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} [{self.position_slug}] - {status}"

    class Meta:
        verbose_name = "Advertisement Slot"
        verbose_name_plural = "Advertisement Slots"
