import unittest
from unittest.mock import MagicMock
from XrayTestRunner.XrayTestRunnerFile import XrayTestRunnerFile, IFileStorage


class TestXrayTestRunnerFile(unittest.TestCase):

    def setUp(self):
        """Set up a mock file storage for testing."""
        self.mock_storage = MagicMock(spec=IFileStorage)
        self.xray_file = XrayTestRunnerFile(self.mock_storage)

    def test_save_calls_storage(self):
        """Test that `save` correctly delegates to the storage implementation."""
        self.xray_file.save("test.txt", "/fake/path", "sample data")
        
        # Verify that the storage's save method was called with correct parameters
        self.mock_storage.save.assert_called_once_with("test.txt", "/fake/path", "sample data")

    def test_save_handles_storage_error(self):
        """Test error handling when storage fails."""
        self.mock_storage.save.side_effect = OSError("Mocked file write error")

        with self.assertRaises(OSError) as context:
            self.xray_file.save("error.txt", "/fake/path", "sample data")

        self.assertEqual(str(context.exception), "Mocked file write error")


if __name__ == "__main__":
    unittest.main()
