import os
from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy.exc import IntegrityError
from .db.database import engine, SessionLocal, init_db
from trip.db.models import Hotel


class HotelImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Generate a file path for each image
        city_name = item.get("city_name", "unknown").lower().replace(" ", "_")
        hotel_name = item.get("property_title", "hotel").lower().replace(" ", "_")
        filename = f"{hotel_name}_{os.path.basename(request.url)}"
        return f"images/{city_name}/{filename}"

    def item_completed(self, results, item, info):
        # Retrieve and store the image path
        image_paths = [x["path"] for ok, x in results if ok]
        if image_paths:
            item["image_path"] = image_paths[0]  # Store the first image path
        return item


class PostgresPipeline:
    def __init__(self):
        # Create tables if they don't exist
        init_db()

    def open_spider(self, spider):
        # Open a database session
        self.session = SessionLocal()

    def close_spider(self, spider):
        # Close the database session
        self.session.close()

    def process_item(self, item, spider):
        try:
            hotel = Hotel(
            property_title=item.get("property_title"),
            city_name=item.get("city_name"),
            hotel_id=item.get("hotel_id"),
            price=item.get("price"),
            rating=item.get("rating"),
            address=item.get("address"),
            latitude=item.get("latitude"),
            longitude=item.get("longitude"),
            room_type=item.get("room_type"),
            image=item.get("image"),
            )
            self.session.add(hotel)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Failed to save hotel: {e}")
         