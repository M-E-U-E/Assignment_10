from django.db import models

class Hotel(models.Model):
    property_title = models.CharField(max_length=255, default="Untitled Hotel")
    description = models.TextField(null=True, blank=True, default="No description available.")
    city_name = models.CharField(max_length=255)  # City where the hotel is located
    hotel_id = models.CharField(max_length=255, unique=True)  # Unique identifier for the hotel
    price = models.FloatField(null=True, blank=True)  # Price of the hotel room
    rating = models.CharField(max_length=255, null=True, blank=True)  # Rating of the hotel
    address = models.CharField(max_length=255, null=True, blank=True)  # Address of the hotel
    latitude = models.FloatField(null=True, blank=True)  # Latitude of the hotel location
    longitude = models.FloatField(null=True, blank=True)  # Longitude of the hotel location
    room_type = models.CharField(max_length=255, null=True, blank=True)  # Room type (e.g., deluxe, suite)
    image = models.CharField(max_length=255, null=True, blank=True)  # Path to the image of the hotel
    description = models.TextField(null=True, blank=True)  # Property description

    class Meta:
        db_table = "hotels"

    def __str__(self):
        return self.property_title




class Summary(models.Model):
    property = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="summaries")
    summary = models.TextField()

class PropertyRating(models.Model):
    property = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="ratings")
    rating = models.FloatField()
    review = models.TextField()