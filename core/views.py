# ----------------------------------------------------------
# core/views.py — Clean, Optimized & Non-Duplicated
# ----------------------------------------------------------

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Vendor, VendorCategory, GalleryImage, ContactMessage


# ----------------------------------------------------------
# CONSTANT — Budget Ranges Per Vendor Category
# ----------------------------------------------------------
CATEGORY_BUDGET_RANGES = {
    "catering": {"min": 150, "max": 2500, "step": 50, "unit": "per plate"},
    "photography": {"min": 10000, "max": 300000, "step": 1000, "unit": "per day"},
    "venue": {"min": 50000, "max": 1000000, "step": 5000, "unit": "total"},
    "decor": {"min": 20000, "max": 500000, "step": 5000, "unit": "total"},
    "makeup artist": {"min": 2000, "max": 50000, "step": 500, "unit": "package"},
}

# ----------------------------------------------------------
# HOME PAGE
# ----------------------------------------------------------
def home(request):
    return render(request, "index.html")


# ----------------------------------------------------------
# VENDORS PAGE — Full Backend Filtering
# ----------------------------------------------------------
def vendors(request):

    category = request.GET.get("category", "all")
    location = request.GET.get("location", "all")
    rating = request.GET.get("rating", "all")
    budget = request.GET.get("budget", "all")

    qs = Vendor.objects.all()

    # ------------------------
    # CATEGORY FILTER
    # ------------------------
    if category != "all":
        qs = qs.filter(category__name__iexact=category)

    # ------------------------
    # LOCATION FILTER
    # ------------------------
    if location != "all":
        qs = qs.filter(location__iexact=location)

    # ------------------------
    # RATING FILTER
    # ------------------------
    if rating != "all":
        try:
            qs = qs.filter(rating__gte=float(rating))
        except:
            pass

    # ------------------------
    # BUDGET FILTER
    # ------------------------
    if budget != "all":
        try:
            qs = qs.filter(average_price__lte=int(budget))
        except:
            pass

    # ------------------------
    # BUDGET SLIDER CONFIG
    # ------------------------
    CATEGORY_BUDGET_RANGES = {
        "venue": {"min": 50000, "max": 2000000, "step": 10000, "unit": "INR"},
        "photography": {"min": 5000, "max": 300000, "step": 5000, "unit": "INR"},
        "decor": {"min": 10000, "max": 500000, "step": 5000, "unit": "INR"},
        "makeup artist": {"min": 2000, "max": 50000, "step": 1000, "unit": "INR"},
        "catering": {"min": 200, "max": 3000, "step": 50, "unit": "₹ per plate"},
    }

    selected_category_key = category.lower() if category else "all"

    budget_ui = CATEGORY_BUDGET_RANGES.get(
        selected_category_key,
        {"min": 0, "max": 100000, "step": 1000, "unit": "INR"}
    )

    # ------------------------
    # FIX LOCATION DUPLICATES
    # ------------------------
    locations = (
        Vendor.objects
        .values_list("location", flat=True)
        .distinct()
        .order_by("location")          # 🔥 avoids duplicates & sorts alphabetically
    )

    # ------------------------
    # CATEGORIES FOR DROPDOWN
    # ------------------------
    categories = VendorCategory.objects.order_by("name")

    return render(request, "vendors.html", {
        "vendors": qs,
        "categories": categories,
        "locations": locations,
        "selected_category": category,
        "selected_location": location,
        "selected_budget": budget,
        "selected_rating": rating,
        "budget_ui": budget_ui,
    })

from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def vendors_by_category(request):
    """
    Returns JSON of vendors given a category name (GET ?category=Photography).
    Used by frontend JS to populate the "vendor" select when user picks a category.
    """
    category_name = request.GET.get("category")
    if not category_name or category_name == "all":
        # return all vendors
        qs = Vendor.objects.all().order_by("-rating", "name")
    else:
        qs = Vendor.objects.filter(category__name__iexact=category_name).order_by("-rating", "name")

    data = []
    for v in qs:
        data.append({
            "id": v.pk,
            "name": v.name,
            "slug": v.slug,
            # include type-specific price if you want on the client
            "price": v.get_price_for_slider(),
        })

    return JsonResponse({"vendors": data})

# ----------------------------------------------------------
# VENDOR DETAILS PAGE
# ----------------------------------------------------------
def vendor_details(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    images = vendor.images.all()  # from related_name="images"

    return render(request, "vendor_details.html", {
        "vendor": vendor,
        "images": images,
    })


# ----------------------------------------------------------
# GALLERY
# ----------------------------------------------------------
def gallery(request):
    return render(request, "gallery.html", {
        "gallery": GalleryImage.objects.all()
    })


# ----------------------------------------------------------
# ABOUT PAGE
# ----------------------------------------------------------
def about(request):
    return render(request, "about.html")


# ----------------------------------------------------------
# CONTACT PAGE
# ----------------------------------------------------------
def contact(request):
    categories = VendorCategory.objects.all()
    return render(request, "contact.html", {"categories": categories})


# ----------------------------------------------------------
# CONTACT FORM HANDLER
# ----------------------------------------------------------
def send_message(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject") or f"Booking request from {name}"
        message = request.POST.get("message")
        preferred_week = request.POST.get("week")
        theme_color = request.POST.get("theme")
        vendor_type = request.POST.get("vendor_type")  # category name
        vendor_slug = request.POST.get("vendor_slug")  # slug of the chosen vendor
        vendor_name = None

        if vendor_slug:
            try:
                vendor = Vendor.objects.get(slug=vendor_slug)
                vendor_name = vendor.name
            except Vendor.DoesNotExist:
                vendor = None

        # Save with extra fields (ensure your model has fields or store as text)
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message or "",
            preferred_week=preferred_week,
            theme_color=theme_color,
            # if your ContactMessage model has vendor_type/vendor_name fields:
            # vendor_type=vendor_type, vendor_name=vendor_name
        )

        messages.success(request, "Your booking request has been sent!")
        return redirect("contact")

    return redirect("contact")

# ----------------------------------------------------------
# LOGIN
# ----------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ----------------------------------------------------------
# REGISTER
# ----------------------------------------------------------
def register_view(request):
    errors = []

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # VALIDATION
        if not all([username, email, password1, password2]):
            errors.append("All fields are required.")

        if User.objects.filter(username=username).exists():
            errors.append("Username already taken.")

        if User.objects.filter(email=email).exists():
            errors.append("Email already registered.")

        if password1 != password2:
            errors.append("Passwords do not match.")

        if len(password1) < 6:
            errors.append("Password must be at least 6 characters long.")

        # SUCCESS → CREATE USER
        if not errors:
            User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, "Account created! Please log in.")
            return redirect("login")

        return render(request, "register.html", {"errors": errors})

    return render(request, "register.html")


# ----------------------------------------------------------
# LOGOUT
# ----------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect("home")


# ----------------------------------------------------------
# DASHBOARD
# ----------------------------------------------------------
@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "saved_vendors": request.user.saved_vendors.all(),
    })


# ----------------------------------------------------------
# SAVE / UNSAVE Vendor (Toggle)
# ----------------------------------------------------------
@login_required
def save_vendor(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)

    if request.user in vendor.saved_by.all():
        vendor.saved_by.remove(request.user)
    else:
        vendor.saved_by.add(request.user)

    return redirect("vendor_details", slug=slug)
