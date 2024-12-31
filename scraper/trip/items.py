from sqlalchemy import Column, Integer, String, Float, Text
from .db.database import Base

# Define SQLAlchemy Hotel Table Model
class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_title = Column(String, nullable=False)  # Matches 'property_title' in Scrapy
    city_name = Column(String, nullable=False)
    hotel_id = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=True)  # Nullable to allow empty prices
    rating = Column(Float, nullable=True)  # Nullable to allow empty ratings
    address = Column(Text, nullable=True)  # Matches 'address' in Scrapy
    latitude = Column(Float, nullable=True)  # Nullable for missing latitudes
    longitude = Column(Float, nullable=True)  # Nullable for missing longitudes
    room_type = Column(String, nullable=True)
    image_url = Column(String, nullable=True)  # Matches 'image' in Scrapy
    image_path = Column(String, nullable=True)  # Path to the stored image
