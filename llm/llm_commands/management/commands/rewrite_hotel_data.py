# llm_commands/management/commands/rewrite_hotel_data.py

import os
import re
import requests
import time
import logging
from django.core.management.base import BaseCommand
from llm_commands.models import Hotel  # Replace with your actual app name
from decouple import config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logging
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("rewrite_hotel.log"),
    ],
)

class Command(BaseCommand):
    help = "Rewrite hotel property titles and descriptions using the Gemini API"

    def __init__(self):
        super().__init__()
        self.api_key = config('GEMINI_API_KEY')
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
            
            # Log the raw response for debugging
            logging.debug(f"Raw API Response: {response.text}")
            
            if response.status_code == 400:
                logging.error(f"Bad Request Error: {response.text}")
                return None
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            return None

    def create_prompt(self, hotel):
        """Create a prompt for the API, handling missing data."""
        title = hotel.property_title if hotel.property_title else "Untitled Property"
        description = hotel.description if hotel.description else "No description available"
        
        return f"""
        As a luxury hotel marketing expert, rewrite the following hotel information to be more appealing and professional.
        
        Current Title: {title}
        Current Description: {description}
        
        Requirements:
        1. Provide ONLY the new title and description
        2. Format your response EXACTLY as shown below:
        Title: [new title]
        Description: [new description]
        
        The title should be eye-catching and memorable (max 50 characters).
        The description should be detailed, engaging, and at least 200 words.
        Do not include any other text or explanations in your response.
        """

    def extract_content(self, api_response):
        """Extract title and description from API response with improved parsing."""
        if not api_response:
            logging.error("No API response received")
            return None, None
            
        try:
            # Log the response structure for debugging
            logging.debug(f"Parsing API response: {api_response}")
            
            # Get the generated text from the response
            if "candidates" in api_response:
                text = api_response["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logging.error("Unexpected API response structure")
                return None, None
            
            # Log the extracted text
            logging.debug(f"Extracted text from response: {text}")
            
            title = None
            description = None
            
            # Split the text into lines and process each line
            lines = text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.lower().startswith('title:'):
                    title = line[6:].strip()
                    current_section = 'title'
                elif line.lower().startswith('description:'):
                    description = line[12:].strip()
                    current_section = 'description'
                elif line and current_section == 'description':
                    # Append additional description lines
                    description = f"{description} {line.strip()}"
            
            # Log the extracted content
            logging.debug(f"Extracted title: {title}")
            logging.debug(f"Extracted description: {description}")
            
            if not title or not description:
                logging.error("Failed to extract title or description")
                return None, None
                
            return title, description
            
        except Exception as e:
            logging.error(f"Error parsing API response: {str(e)}")
            return None, None

    def handle(self, *args, **options):
        """Main command handler."""
        hotels = Hotel.objects.all()
        total = hotels.count()
        processed = 0
        skipped = 0
        updated = 0
        
        self.stdout.write(f"Starting to process {total} hotels...")
        
        for hotel in hotels:
            processed += 1
            
            # Skip hotels with no data
            if not hotel.property_title and not hotel.description:
                self.stdout.write(f"Skipping hotel {hotel.id}: Missing title and description")
                skipped += 1
                continue
                
            try:
                # Create prompt and call API
                prompt = self.create_prompt(hotel)
                api_response = self.call_gemini_api(prompt)
                
                if api_response:
                    new_title, new_description = self.extract_content(api_response)
                    
                    if new_title and new_description:
                        # Store original values for logging
                        original_title = hotel.property_title
                        original_description = hotel.description
                        
                        # Update hotel
                        hotel.property_title = new_title
                        hotel.description = new_description
                        hotel.save()
                        
                        updated += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Updated hotel {hotel.id} ({processed}/{total})"
                            )
                        )
                        
                        # Log the changes
                        logging.info(f"Hotel {hotel.id} updated:")
                        logging.info(f"Original title: {original_title}")
                        logging.info(f"New title: {new_title}")
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Failed to update hotel {hotel.id} ({processed}/{total}): Invalid content"
                            )
                        )
                        skipped += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Failed to update hotel {hotel.id} ({processed}/{total}): API error"
                        )
                    )
                    skipped += 1
                
                # Add delay between API calls
                time.sleep(2)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error processing hotel {hotel.id}: {str(e)}"
                    )
                )
                logging.error(f"Error processing hotel {hotel.id}: {str(e)}")
                skipped += 1
                continue
        
        # Print final statistics
        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Processing completed:
                - Total hotels: {total}
                - Successfully updated: {updated}
                - Skipped: {skipped}
                """
            )
        )