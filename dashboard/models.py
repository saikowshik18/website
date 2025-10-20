from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('books', 'Books'),
        ('furniture', 'Furniture'),
        ('clothing', 'Clothing'),
        ('other', 'Other'),
    ]

    LOCATION_CHOICES = [
        ('bh1-front', 'BH1 Front'),
        ('bh1-back', 'BH1 Back'),
        ('bh2-front', 'BH2 Front'),
        ('bh2-back', 'BH2 Back'),
        ('gh1-front', 'GH1 Front'),
        ('gh1-back', 'GH1 Back'),
        ('gh2-front', 'GH2 Front'),
        ('gh2-back', 'GH2 Back'),
        ('old-campus', 'Old Campus'),
    ]

    FLOOR_CHOICES = [
        ('ground', 'Ground Floor'),
        ('first', 'First Floor'),
        ('second', 'Second Floor'),
        ('third', 'Third Floor'),
    ]

    # Linked user (nullable for existing data, can make non-null later)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="products")

    # Product details
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)

    # Location details
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    floor = models.CharField(max_length=20, choices=FLOOR_CHOICES)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    wing = models.CharField(max_length=50, blank=True, null=True)

    # Contact info
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    # Meta info
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    academic_year = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.category}"




from django.db import models
from django.contrib.auth.models import User
from .models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"
