from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ----------------------------------------------------------
# Vendor Category
# ----------------------------------------------------------
class VendorCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Vendor Category"
        verbose_name_plural = "Vendor Categories"

    def __str__(self):
        return self.name


# ----------------------------------------------------------
# Vendor Model — Supports All Vendor Types
# ----------------------------------------------------------
class Vendor(models.Model):

    # Basic Vendor Info
    category = models.ForeignKey(
        VendorCategory,
        on_delete=models.CASCADE,
        related_name="vendors"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=120)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='vendors/')

    # Save / Unsave (Dashboard Feature)
    saved_by = models.ManyToManyField(
        User,
        related_name="saved_vendors",
        blank=True
    )

    # -------------------------------
    # Category-specific pricing fields
    # (Used by filtering + vendor details)
    # -------------------------------
    price_per_plate = models.PositiveIntegerField(
        default=0,
        help_text="INR per plate (Catering)"
    )
    price_per_day = models.PositiveIntegerField(
        default=0,
        help_text="INR per day (Photography)"
    )
    average_price = models.PositiveIntegerField(
        default=0,
        help_text="Average booking price (Venue)"
    )
    decor_price = models.PositiveIntegerField(
        default=0,
        help_text="Decor package price (Decor)"
    )
    makeup_price = models.PositiveIntegerField(
        default=0,
        help_text="Makeup package price (Makeup Artist)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-rating", "name")

    # Automatic Unique Slug Generator
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1

            # Ensure uniqueness
            while Vendor.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    # Universal price fetcher for sliders + UI
    def get_price_for_slider(self):
        cat = (self.category.name or "").lower()

        if "cater" in cat:
            return self.price_per_plate
        if "photo" in cat:
            return self.price_per_day
        if "venue" in cat:
            return self.average_price
        if "decor" in cat:
            return self.decor_price
        if "makeup" in cat:
            return self.makeup_price

        return 0

    def __str__(self):
        return self.name


# ----------------------------------------------------------
# Vendor Gallery Images (Detail Page Carousel)
# ----------------------------------------------------------
class VendorImage(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="vendor_gallery/")

    def __str__(self):
        return f"{self.vendor.name} Image"


# ----------------------------------------------------------
# General Site Gallery
# ----------------------------------------------------------
class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ("ceremony", "Ceremony"),
        ("reception", "Reception"),
        ("decor", "Decor"),
        ("haldi", "Haldi / Mehendi"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return f"{self.category} image"


# ----------------------------------------------------------
# Contact Form Messages
# ----------------------------------------------------------
# core/models.py


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    week = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    vendor_type = models.CharField(max_length=120, blank=True, null=True)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    preferred_week = models.CharField(max_length=50, null=True, blank=True)
    theme_color = models.CharField(max_length=20, null=True, blank=True)
   # REQUIRED

    def __str__(self):
        return f"{self.name} - {self.subject}"

