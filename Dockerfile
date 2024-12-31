FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /usr/src/scraper

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copy the requirements.txt to install dependencies
COPY requirements.txt /usr/src/scraper/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Scrapy project into the container
COPY ./scraper /usr/src/scraper/

# Default command to run the Scrapy spider
CMD ["scrapy", "crawl", "async_trip"]
