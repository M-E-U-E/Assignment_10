from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from llm_commands.models import Hotel, Summary, PropertyRating

class RewriteHotelDataCommandTestCase(TestCase):
    def setUp(self):
        # Create test hotels
        self.hotel1 = Hotel.objects.create(
            property_title="Test Hotel 1",
            description="A wonderful place to stay.",
        )
        self.hotel2 = Hotel.objects.create(
            property_title="Test Hotel 2",
            description="",
        )

    @patch('llm_commands.management.commands.rewrite_hotel_data.Command.call_gemini_api')
    def test_rewrite_hotel_data(self, mock_call_gemini_api):
        # Mock Gemini API response
        mock_call_gemini_api.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "Title: Updated Title\nDescription: Updated Description"}]}}
            ]
        }

        # Run the management command
        call_command('rewrite_hotel_data')

        # Refresh hotel objects
        self.hotel1.refresh_from_db()

        # Assertions for the first hotel
        self.assertEqual(self.hotel1.property_title, "Updated Title")
        self.assertEqual(self.hotel1.description, "Updated Description")

        # Ensure skipped hotel
        self.assertEqual(self.hotel2.description, "")

class GenerateSummariesAndRatingsTestCase(TestCase):
    def setUp(self):
        # Create test hotels
        self.hotel = Hotel.objects.create(
            property_title="Test Hotel",
            description="A cozy place to enjoy your vacation.",
        )

    @patch('llm_commands.management.commands.generate_summaries_and_ratings.Command.call_gemini_api')
    def test_generate_summaries_and_ratings(self, mock_call_gemini_api):
        # Mock responses for summary and rating
        mock_call_gemini_api.side_effect = [
            {"candidates": [{"content": {"parts": [{"text": "A cozy and relaxing getaway"}]}}]},
            {"candidates": [{"content": {"parts": [{"text": "Rating: 4.5\nReview: Excellent service and facilities."}]}}]},
        ]

        # Run the management command
        call_command('generate_summaries_and_ratings')

        # Verify summary creation
        summary = Summary.objects.filter(property=self.hotel).first()
        self.assertIsNotNone(summary)
        self.assertEqual(summary.summary, "A cozy and relaxing getaway")

        # Verify property rating creation
        rating = PropertyRating.objects.filter(property=self.hotel).first()
        self.assertIsNotNone(rating)
        self.assertEqual(rating.rating, 4.5)
        self.assertEqual(rating.review, "Excellent service and facilities.")

class UtilityFunctionsTestCase(TestCase):
    @patch('llm_commands.management.commands.generate_summaries_and_ratings.Command.call_gemini_api')
    def test_call_gemini_api(self, mock_call_gemini_api):
        # Mock API response
        mock_call_gemini_api.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "Generated content from Gemini API"}]}}
            ]
        }

        # Call the method
        command = MagicMock()
        response = command.call_gemini_api("Test Prompt")

        # Assertions
        self.assertIsNotNone(response)
        self.assertIn("candidates", response)

    def test_parse_rating_review(self):
        from llm_commands.management.commands.generate_summaries_and_ratings import parse_rating_review

        # Valid response
        valid_response = "Rating: 5\nReview: Excellent property!"
        rating, review = parse_rating_review(valid_response)
        self.assertEqual(rating, 5)
        self.assertEqual(review, "Excellent property!")

        # Invalid response
        invalid_response = "Invalid data"
        with self.assertRaises(ValueError):
            parse_rating_review(invalid_response)

        # Missing rating
        no_rating_response = "Review: Excellent property!"
        with self.assertRaises(ValueError):
            parse_rating_review(no_rating_response)

        # Missing review
        no_review_response = "Rating: 4"
        with self.assertRaises(ValueError):
            parse_rating_review(no_review_response)

    def test_truncate_text(self):
        from llm_commands.management.commands.generate_summaries_and_ratings import truncate_text

        # Short text
        text = "This is a short text."
        self.assertEqual(truncate_text(text, 50), text)

        # Text requiring truncation
        text = "This is a long text that needs truncation."
        self.assertEqual(truncate_text(text, 20), "This is a long...")

    def test_extract_first_title(self):
        from llm_commands.management.commands.generate_summaries_and_ratings import extract_first_title

        # Valid title
        text = "**Great Title**\nMore text"
        self.assertEqual(extract_first_title(text), "Great Title")

        # No valid title
        invalid_text = "No valid title here."
        with self.assertRaises(ValueError):
            extract_first_title(invalid_text)
