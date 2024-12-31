#!/bin/sh

if [ "$SERVICE" = "django" ]; then
  echo "Starting Django service..."
  wait-for-it db:5432 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000
elif [ "$SERVICE" = "scrapy" ]; then
  echo "Starting Scrapy service..."
  cd /usr/src/scraper && scrapy crawl async_trip
else
  echo "Invalid service specified. Please set the SERVICE environment variable to 'django' or 'scrapy'."
  exit 1
fi
