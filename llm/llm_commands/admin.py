from django.contrib import admin
from .models import Hotel, Summary, PropertyRating

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("property_title", "city_name", "price", "rating")
    search_fields = ("property_title", "city_name")
    list_filter = ("city_name", "rating")


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("property", "summary")
    search_fields = ("property__property_title",)


@admin.register(PropertyRating)
class PropertyRatingAdmin(admin.ModelAdmin):
    list_display = ("property", "rating", "review")
    search_fields = ("property__property_title", "review")
    list_filter = ("rating",)
