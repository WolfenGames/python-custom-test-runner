import unittest
from unittest.mock import patch, MagicMock
from XrayTestRunner.TestBase import TestBase
from requests import Response

class TestTestBase(unittest.TestCase):

    def setUp(self):
        """Set up a TestBase instance for testing."""
        self.test_base = TestBase(url="https://api.example.com")

    @patch("src.TestBase.request")
    def test_send_request_success(self, mock_request):
        """Test send_request method for a successful response."""
        # Mock a successful response
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "success"}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_request.return_value = mock_response

        # Call send_request
        response = self.test_base.send_request("GET", "/test-endpoint")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "success"})
        self.assertEqual(response.headers["Content-Type"], "application/json")

    @patch("src.TestBase.request")
    def test_send_request_failure(self, mock_request):
        """Test send_request method when the API returns an error."""
        # Mock an error response
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.headers = {}
        mock_request.return_value = mock_response

        # Call send_request
        response = self.test_base.send_request("POST", "/fail-endpoint", data={"key": "value"})

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.text, "Internal Server Error")
        self.assertEqual(response.headers, {})
    @patch("src.TestBase.request")
    def test_send_request_exception_handling(self, mock_request):
        """Test send_request handles request exceptions properly."""
        # Mock an exception during request
        mock_request.side_effect = Exception("Network Error")

        with self.assertRaises(Exception) as context:
            self.test_base.send_request("GET", "/exception-endpoint")

        # Assertions
        self.assertEqual(str(context.exception), "Network Error")

if __name__ == "__main__":
    unittest.main()
