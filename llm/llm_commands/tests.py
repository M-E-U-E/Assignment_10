import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up Django environment for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llm.settings')
import django
django.setup()

from llm_commands.management.commands.rewrite_hotel_data import Command as RewriteCommand
from llm_commands.management.commands.generate_summaries_and_ratings import Command as GenerateCommand
from llm_commands.models import Hotel, Summary, PropertyRating


class TestRewriteHotelDataCommand(unittest.TestCase):
    def setUp(self):
        self.hotel = MagicMock(
            id=1,
            property_title="Old Hotel Title",
            description="This is the old description."
        )

    @patch('llm_commands.management.commands.rewrite_hotel_data.Command.call_gemini_api')
    def test_rewrite_hotel_data_success(self, mock_call_gemini_api):
        mock_call_gemini_api.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Title: New Hotel Title\nDescription: This is the new description."}]}}]
        }
        command = RewriteCommand()
        title, description = command.extract_content(mock_call_gemini_api.return_value)
        self.assertEqual(title, "New Hotel Title")
        self.assertEqual(description, "This is the new description.")

    @patch('llm_commands.management.commands.rewrite_hotel_data.Command.call_gemini_api')
    def test_rewrite_hotel_data_api_error(self, mock_call_gemini_api):
        mock_call_gemini_api.side_effect = Exception("API error")
        command = RewriteCommand()
        title, description = command.extract_content(None)
        self.assertIsNone(title)
        self.assertIsNone(description)
    
    def test_create_prompt_with_complete_data(self):
        command = RewriteCommand()
        prompt = command.create_prompt(self.hotel)
        self.assertIn("Old Hotel Title", prompt)
        self.assertIn("This is the old description.", prompt)
    
    def test_handle_with_api_error(self):
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__iter__.return_value = iter([self.hotel])
        with patch('llm_commands.models.Hotel.objects.all', return_value=mock_queryset):
            with patch('llm_commands.management.commands.rewrite_hotel_data.Command.call_gemini_api', side_effect=Exception("API error")):
                command = RewriteCommand()
                command.stdout = MagicMock()
                command.handle()
                any_error_call = any(
                    "Error processing hotel 1: API error" in call[0][0]
                    for call in command.stdout.write.call_args_list
                )
                self.assertTrue(any_error_call, "Expected error message not found in output")

    def test_rewrite_hotel_data_no_response(self):
        command = RewriteCommand()
        title, description = command.extract_content(None)
        self.assertIsNone(title)
        self.assertIsNone(description)

    def test_create_prompt_with_missing_fields(self):
        incomplete_hotel = MagicMock(property_title=None, description=None)
        command = RewriteCommand()
        prompt = command.create_prompt(incomplete_hotel)
        self.assertIn("Untitled Property", prompt)
        self.assertIn("No description available", prompt)

    def test_extract_content_with_invalid_response(self):
        command = RewriteCommand()
        invalid_response = {"unexpected": "structure"}
        title, description = command.extract_content(invalid_response)
        self.assertIsNone(title)
        self.assertIsNone(description)

    def test_handle_with_no_hotels(self):
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 0
        with patch('llm_commands.models.Hotel.objects.all', return_value=mock_queryset):
            command = RewriteCommand()
            command.stdout = MagicMock()
            command.handle()
            command.stdout.write.assert_any_call(
                '\x1b[32;1m\n                Processing completed:\n'
                '                - Total hotels: 0\n'
                '                - Successfully updated: 0\n'
                '                - Skipped: 0\n                \x1b[0m'
            )


class TestGenerateSummariesAndRatingsCommand(unittest.TestCase):
    def setUp(self):
        self.hotel = MagicMock(
            id=1,
            property_title="Sample Hotel",
            description="This is a sample description."
        )
    
    @patch('llm_commands.management.commands.generate_summaries_and_ratings.Command.call_gemini_api')
    def test_generate_summary_success(self, mock_call_gemini_api):
        mock_call_gemini_api.return_value = {
            "candidates": [{"content": {"parts": [{"text": "This is a summary of the hotel."}]}}]
        }
        command = GenerateCommand()
        summary_prompt = command.generate_summary_prompt(self.hotel)
        response = command.call_gemini_api(summary_prompt)
        summary_text = response["candidates"][0]["content"]["parts"][0]["text"]
        self.assertEqual(summary_text, "This is a summary of the hotel.")

    def test_parse_rating_review_with_invalid_format(self):
        command = GenerateCommand()
        invalid_text = "Invalid text without rating or review"
        rating, review = command.parse_rating_review(invalid_text)
        self.assertIsNone(rating)
        self.assertIsNone(review)

    @patch('llm_commands.management.commands.generate_summaries_and_ratings.Command.call_gemini_api')
    def test_generate_rating_and_review_success(self, mock_call_gemini_api):
        mock_call_gemini_api.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Rating: 4.5\nReview: Excellent stay with great service!"}]}}]
        }
        command = GenerateCommand()
        rating_prompt = command.generate_rating_prompt(self.hotel)
        response = command.call_gemini_api(rating_prompt)
        rating, review = command.parse_rating_review(response["candidates"][0]["content"]["parts"][0]["text"])
        self.assertEqual(rating, 4.5)
        self.assertEqual(review, "Excellent stay with great service!")

    def test_generate_rating_prompt(self):
        command = GenerateCommand()
        prompt = command.generate_rating_prompt(self.hotel)
        self.assertIn("Sample Hotel", prompt)
        self.assertIn("This is a sample description.", prompt)

    @patch('llm_commands.management.commands.generate_summaries_and_ratings.Command.call_gemini_api')
    def test_handle_with_api_timeout(self):
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__iter__.return_value = iter([self.hotel])
        with patch('llm_commands.models.Hotel.objects.all', return_value=mock_queryset):
            with patch('llm_commands.management.commands.generate_summaries_and_ratings.Command.call_gemini_api', side_effect=Exception("Timeout")):
                command = GenerateCommand()
                command.stdout = MagicMock()
                command.handle()
                any_error_call = any(
                    "Error processing hotel 1: Timeout" in call[0][0]
                    for call in command.stdout.write.call_args_list
                )
                self.assertTrue(any_error_call, "Expected error message not found in output")
        
    # If no exception was raised, fail the test
    def test_generate_summary_prompt_with_partial_data(self):
        incomplete_hotel = MagicMock(property_title="Sample Hotel", description=None)
        command = GenerateCommand()
        prompt = command.generate_summary_prompt(incomplete_hotel)
        self.assertIn("Sample Hotel", prompt)
        self.assertIn("Description: None", prompt)

    def test_parse_rating_review_missing_fields(self):
        command = GenerateCommand()
        invalid_text = "Rating: \nReview: "
        rating, review = command.parse_rating_review(invalid_text)
        self.assertIsNone(rating)
        self.assertIsNone(review)

    def test_handle_with_missing_data(self):
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__iter__.return_value = iter([
            MagicMock(property_title=None, description=None, id=1)
        ])
        with patch('llm_commands.models.Hotel.objects.all', return_value=mock_queryset):
            command = GenerateCommand()
            command.stdout = MagicMock()
            command.handle()
            command.stdout.write.assert_any_call("Skipping hotel 1: Missing title or description")

    def test_handle_with_api_timeout(self):
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__iter__.return_value = iter([self.hotel])
        with patch('llm_commands.models.Hotel.objects.all', return_value=mock_queryset):
            with patch('llm_commands.management.commands.generate_summaries_and_ratings.Command.call_gemini_api', side_effect=Exception("Timeout")):
                command = GenerateCommand()
                command.stdout = MagicMock()
                command.handle()
                any_error_call = any(
                    "Error processing hotel 1: Timeout" in call[0][0]
                    for call in command.stdout.write.call_args_list
                )
                self.assertTrue(any_error_call, "Expected error message not found in output")


if __name__ == '__main__':
    unittest.main()
