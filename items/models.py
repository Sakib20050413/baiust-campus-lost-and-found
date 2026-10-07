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
        cat_name = self.category.name.lower() if self.category else ''
        if 'electronic' in cat_name:
            return 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=60'
        elif 'card' in cat_name or 'id' in cat_name:
            return 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=60'
        elif 'book' in cat_name or 'notebook' in cat_name:
            return 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500&auto=format&fit=crop&q=60'
        elif 'wallet' in cat_name or 'money' in cat_name:
            return 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&auto=format&fit=crop&q=60'
        return 'https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=500&auto=format&fit=crop&q=60'

