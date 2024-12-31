BOT_NAME = 'trip'

SPIDER_MODULES = ['trip.spiders']
NEWSPIDER_MODULE = 'trip.spiders'

ITEM_PIPELINES = {
    'trip.pipelines.PostgresPipeline': 300,
}


IMAGES_STORE = 'city_data/images_of_hotels'

DATABASE_URL = 'postgresql://username:password@db:5432/hotel_db' 
