from django.contrib import admin
from .models import (
    Vendor,
    VendorCategory,
    VendorImage,
    GalleryImage,
    ContactMessage,
)

# -----------------------------------------------------
# Inline model for Vendor Images (Multiple Images per Vendor)
# -----------------------------------------------------
class VendorImageInline(admin.TabularInline):
    model = VendorImage
    extra = 3


# -----------------------------------------------------
# Vendor Admin Panel
# -----------------------------------------------------
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "location", "rating", "get_main_price")
    list_filter = ("category", "location")
    search_fields = ("name", "location", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [VendorImageInline]

    def get_main_price(self, obj):
        return obj.get_price_for_slider()
    get_main_price.short_description = "Price"


# -----------------------------------------------------
# Vendor Category Admin
# -----------------------------------------------------
@admin.register(VendorCategory)
class VendorCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


# -----------------------------------------------------
# Gallery Images Admin
# -----------------------------------------------------
@admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("category", "image")
    list_filter = ("category",)


# -----------------------------------------------------
# Contact Messages Admin
# -----------------------------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    ordering = ("-created_at",)
