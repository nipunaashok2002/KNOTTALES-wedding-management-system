from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vendors/', views.vendors, name='vendors'),
    path('vendor/<slug:slug>/', views.vendor_details, name='vendor_details'),
    path("vendor/<slug:slug>/save/", views.save_vendor, name="save_vendor"),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('api/vendors/', views.vendors_by_category, name='api_vendors_by_category'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Contact Message
    path('send-message/', views.send_message, name='send_message'),

]
