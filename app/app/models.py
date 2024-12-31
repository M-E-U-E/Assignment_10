# llmApp/models.py
from django.db import models

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    property_title = models.CharField(max_length=255)
    hotel_id = models.CharField(max_length=50, unique=True)  # Added unique=True for referential integrity
    price = models.FloatField()
    rating = models.FloatField()
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    room_type = models.CharField(max_length=100)
    image = models.URLField()
    local_image_path = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'hotels'
        managed = False

class PropertySummary(models.Model):
    property = models.ForeignKey(
        'Hotel', 
        to_field='hotel_id',  # Reference the hotel_id field
        db_column='property_id',  # The column name in the database
        on_delete=models.CASCADE, 
        related_name='summaries'
    )
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'property_summaries'

class PropertyReview(models.Model):
    property = models.ForeignKey(
        'Hotel',
        to_field='hotel_id',  # Reference the hotel_id field
        db_column='property_id',  # The column name in the database
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.FloatField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'property_reviews'