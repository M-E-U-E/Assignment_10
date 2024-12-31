from django.contrib import admin
from .models import Hotel, PropertySummary, PropertyReview

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('property_title', 'description', 'city_name', "hotel_id",'price','rating','address','latitude','longitude','room_type','image','local_image_path')
    search_fields = ('property_title', 'city_name', 'address')
    list_filter = ('city_name', 'rating')

@admin.register(PropertySummary)
class PropertySummaryAdmin(admin.ModelAdmin):
    list_display = ('property', 'summary', 'created_at', 'updated_at')
    search_fields = ('property_title', 'summary')
    list_filter = ('created_at', 'updated_at')

@admin.register(PropertyReview)
class PropertyReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'rating', 'review','created_at')
    search_fields = ('property_title', 'review')
    list_filter = ('rating', 'created_at')