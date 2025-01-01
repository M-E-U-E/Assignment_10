import os
import requests
import time
import re
import logging
from django.core.management.base import BaseCommand
from llm_commands.models import Hotel, Summary, PropertyRating
from decouple import config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("generate_summaries_and_ratings.log"),
    ],
)

class Command(BaseCommand):
    help = "Generate summaries, ratings, and reviews for hotels using the Gemini API"

    def __init__(self):
        super().__init__()
        self.api_key = config("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

    def call_gemini_api(self, prompt):
        """Call the Gemini API with proper error handling."""
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }

        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code != 200:
                logging.error(f"API Error: {response.status_code} - {response.text}")
                return None

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            return None

    def generate_summary_prompt(self, hotel):
        """Create a prompt for generating hotel summaries."""
        return f"""
        Provide a concise summary for the following hotel information:

        Title: {hotel.property_title}
        Description: {hotel.description}

        The summary should be professional and limited to 150 words.
        """

    def generate_rating_prompt(self, hotel):
        """Create a prompt for generating hotel ratings and reviews."""
        return f"""
        Based on the following details, provide a rating (0-5) and a review for the hotel:

        Title: {hotel.property_title}
        Description: {hotel.description}

        Format your response as:
        Rating: [rating]
        Review: [review text]
        """

    def parse_rating_review(self, text):
        """Parse rating and review from the API response."""
        try:
            rating_match = re.search(r"Rating:\s*(\d+\.?\d*)", text)
            review_match = re.search(r"Review:\s*(.+)$", text, re.DOTALL)

            if not rating_match or not review_match:
                raise ValueError("Failed to extract rating or review")

            rating = float(rating_match.group(1))
            review = review_match.group(1).strip()
            return rating, review
        except Exception as e:
            logging.error(f"Error parsing rating/review: {str(e)}")
            return None, None

    def handle(self, *args, **options):
        """Main command handler."""
        hotels = Hotel.objects.all()
        total = hotels.count()
        updated_summaries = 0
        updated_ratings = 0

        self.stdout.write(f"Starting to process {total} hotels...")

        for hotel in hotels:
            if not hotel.property_title or not hotel.description:
                self.stdout.write(f"Skipping hotel {hotel.id}: Missing title or description")
                continue

            try:
                # Generate summary
                summary_prompt = self.generate_summary_prompt(hotel)
                summary_response = self.call_gemini_api(summary_prompt)

                if summary_response:
                    summary_text = summary_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    if summary_text:
                        Summary.objects.create(property=hotel, summary=summary_text)
                        updated_summaries += 1
                        self.stdout.write(self.style.SUCCESS(f"Generated summary for hotel {hotel.id}"))

                # Generate rating and review
                rating_prompt = self.generate_rating_prompt(hotel)
                rating_response = self.call_gemini_api(rating_prompt)

                if rating_response:
                    rating_text = rating_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    if rating_text:
                        rating, review = self.parse_rating_review(rating_text)
                        if rating is not None and review:
                            PropertyRating.objects.create(property=hotel, rating=rating, review=review)
                            updated_ratings += 1
                            self.stdout.write(self.style.SUCCESS(f"Generated rating and review for hotel {hotel.id}"))

                # Add delay between API calls
                time.sleep(2)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing hotel {hotel.id}: {str(e)}"))
                logging.error(f"Error processing hotel {hotel.id}: {str(e)}")
                continue

        # Final statistics
        self.stdout.write(
            self.style.SUCCESS(
                f"Completed processing hotels:\n - Summaries generated: {updated_summaries}\n - Ratings generated: {updated_ratings}"
            )
        )
