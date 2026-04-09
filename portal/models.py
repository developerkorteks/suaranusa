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

from django.utils.text import slugify
from django.utils import timezone

class ManualArticle(models.Model):
    """
    Manual Article Management for suaranusa.
    Allows creating original content directly via Django Admin.
    """
    CATEGORY_CHOICES = [
        ('NEWS', 'News'),
        ('NASIONAL', 'Nasional'),
        ('INTERNASIONAL', 'Internasional'),
        ('EKONOMI', 'Ekonomi'),
        ('OLAHRAGA', 'Olahraga'),
        ('TEKNOLOGI', 'Teknologi'),
        ('HIBURAN', 'Hiburan'),
        ('GAYA HIDUP', 'Gaya Hidup'),
        ('OTOMOTIF', 'Otomotif'),
        ('TRAVEL', 'Travel'),
        ('VIDEO', 'Video'),
        ('TOPIK KHUSUS', 'Topik Khusus'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    main_image = models.ImageField(upload_to='manual_news/%Y/%m/%d/', help_text="Featured image for the article")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='NEWS')
    content = models.TextField(help_text="Full article content (supports HTML via Summernote)")
    author = models.CharField(max_length=100, default="Redaksi Suaranusa")
    publish_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def to_dict(self):
        """Convert model instance to a dictionary compatible with Scraper API format."""
        return {
            'id': f"m-{self.id}",
            'title': self.title,
            'url': f"/news/{self.id}/{self.slug}/",
            'image': self.main_image.url if self.main_image else None,
            'category': self.category,
            'publish_date': self.publish_date.isoformat(),
            'description': self.content[:200] + "..." if self.content else "",
            'content': self.content,
            'author': self.author,
            'source': "suaranusa.my.id",
            'is_manual': True,
            'scraped_at': self.created_at.isoformat(),
            'metadata': {
                'images': [{'url': self.main_image.url}] if self.main_image else [],
                'is_manual': True
            }
        }

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Manual Article"
        verbose_name_plural = "Manual Articles"
        ordering = ['-publish_date']
