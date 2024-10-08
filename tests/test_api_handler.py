# tests/test_api_handler.py

import unittest
from unittest.mock import patch, MagicMock

import requests

from src.api_handler import APIHandler


class TestAPIHandler(unittest.TestCase):

    @patch('src.api_handler.EmailAlert')
    @patch('src.api_handler.Logger')
    def setUp(self, MockLogger, MockEmailAlert):
        self.mock_logger = MockLogger.return_value
        self.mock_email_alert = MockEmailAlert.return_value
        self.api_handler = APIHandler()

    def test_call_api(self):
        response = self.api_handler.call_api('https://jsonplaceholder.typicode.com/posts', {})
        self.assertIsNotNone(response)

    @patch('requests.get')
    def test_api_call_returns_json_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = self.api_handler.call_api('http://example.com', {'param': 'value'})
        self.assertEqual(response, {'key': 'value'})

    @patch('requests.get', side_effect=requests.exceptions.RequestException('Error'))
    def test_api_call_handles_request_exception(self, mock_get):
        response = self.api_handler.call_api('http://example.com', {'param': 'value'})
        self.assertIsNone(response)
        self.mock_logger.error.assert_called_once_with('API call failed: Error')
        self.mock_email_alert.send_email_alert.assert_called_once_with('API call failed: Error')

    @patch('requests.get')
    def test_api_call_handles_non_200_status_code(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('HTTP Error')
        mock_get.return_value = mock_response

        response = self.api_handler.call_api('http://example.com', {'param': 'value'})
        self.assertIsNone(response)
        self.api_handler.logger.error.assert_called_once_with('API call failed: HTTP Error')
        self.api_handler.email_alert.send_email_alert.assert_called_once_with('API call failed: HTTP Error')

if __name__ == '__main__':
    unittest.main()