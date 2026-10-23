from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

CAMPUS_LOCATIONS = [
    ('Academic Building 1', 'Academic Building 1'),
    ('Academic Building 2', 'Academic Building 2'),
    ('Central Library', 'Central Library'),
    ('Main Cafeteria / Canteen', 'Main Cafeteria / Canteen'),
    ('Boys Hall', 'Boys Hall'),
    ('Girls Hall', 'Girls Hall'),
    ('Playground / Sports Ground', 'Playground / Sports Ground'),
    ('Campus Bus', 'Campus Bus'),
    ('Computer Lab (Lab 1-4)', 'Computer Lab (Lab 1-4)'),
    ('ECE/EEE Lab', 'ECE/EEE Lab'),
    ('Admin Building', 'Admin Building'),
    ('Mosque Area', 'Mosque Area'),
    ('Campus Gate / Reception', 'Campus Gate / Reception'),
    ('Other Campus Location', 'Other Campus Location'),
]

ITEM_TYPE_CHOICES = [
    ('LOST', 'Lost Item'),
    ('FOUND', 'Found Item'),
]

STATUS_CHOICES = [
    ('PENDING', 'Pending Verification'),
    ('APPROVED', 'Active / Listed'),
    ('MATCHED', 'Potential Match Found'),
    ('RETURNED', 'Returned / Resolved'),
]

CUSTODY_CHOICES = [
    ('With Finder', 'With Finder (Keep in own custody)'),
    ('Deposited at Security Office', 'Deposited at Security Office'),
    ('Deposited at Dept Office', 'Deposited at Dept Office'),
    ('Campus Reception / Gate', 'Campus Reception / Gate'),
    ('Central Library Desk', 'Central Library Desk'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default='bi-box-seam', help_text="Bootstrap icon class e.g. bi-laptop, bi-card-text")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=150)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, default='LOST')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    primary_image = models.ImageField(upload_to='items/')
    additional_image = models.ImageField(upload_to='items/additional/', blank=True, null=True)
    location = models.CharField(max_length=100, choices=CAMPUS_LOCATIONS)
    specific_location_details = models.CharField(max_length=255, help_text="e.g. Room 304, 2nd row bench, or Near Water Cooler")
    date_occurred = models.DateField(help_text="Date the item was lost or found")
    description = models.TextField(help_text="Detailed description of color, brand, condition, tags, etc.")
    
    # Found item verification security
    secret_mark_question = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="For FOUND items: Ask a question only the owner can answer (e.g. lock screen wallpaper, inside sticker, contents of purse)"
    )
    current_custody = models.CharField(
        max_length=100, 
        choices=CUSTODY_CHOICES, 
        default='With Finder', 
        blank=True
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_item_type_display()}] {self.title} - {self.location}"

    def get_absolute_url(self):
        return reverse('items:detail', kwargs={'pk': self.pk})

    @property
    def fallback_image_url(self):
        title = self.title.lower() if self.title else ''
        cat_name = self.category.name.lower() if self.category else ''
        
        if 'calculator' in title or 'casio' in title:
            return 'https://images.unsplash.com/photo-1594980596870-8aa52a78d8cd?w=600&auto=format&fit=crop&q=75'
        elif 'charger' in title or 'adapter' in title or 'cable' in title:
            return 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=75'
        elif 'card' in title or 'id' in title or 'student' in title or 'card' in cat_name:
            return 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=75'
        elif 'laptop' in title or 'macbook' in title or 'dell' in title:
            return 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=75'
        elif 'phone' in title or 'mobile' in title or 'iphone' in title or 'samsung' in title:
            return 'https://images.unsplash.com/photo-1511707171634-5f897ff02560?w=600&auto=format&fit=crop&q=75'
        elif 'book' in title or 'notebook' in title or 'book' in cat_name:
            return 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=75'
        elif 'wallet' in title or 'money' in title or 'purse' in title or 'wallet' in cat_name:
            return 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=600&auto=format&fit=crop&q=75'
        elif 'bag' in title or 'backpack' in title or 'bag' in cat_name:
            return 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=75'
        elif 'key' in title or 'keys' in cat_name:
            return 'https://images.unsplash.com/photo-1582139329536-e7284fece509?w=600&auto=format&fit=crop&q=75'
        elif 'electronic' in cat_name:
            return 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=75'
        return 'https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=600&auto=format&fit=crop&q=75'

    @property
    def display_image_url(self):
        if not self.primary_image:
            return self.fallback_image_url
        name = str(self.primary_image.name).lower()
        if 'lost_' in name or 'casio_' in name or 'dell_' in name or 'student_' in name:
            return self.fallback_image_url
        return self.primary_image.url


