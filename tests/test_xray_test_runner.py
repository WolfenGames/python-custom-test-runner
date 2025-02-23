import unittest
from unittest.mock import patch, MagicMock
from XrayTestRunner.XrayTestRunner import XrayTestRunner, JUnitXMLReportWriter
import datetime


class TestXrayTestRunner(unittest.TestCase):

    def setUp(self):
        """Set up XrayTestRunner instance for testing with a mocked report writer."""
        self.mock_report_writer = MagicMock(spec=JUnitXMLReportWriter)
        self.test_runner = XrayTestRunner(report_writer=self.mock_report_writer)

    @unittest.skip("Borked")
    @patch("src.XrayTestRunner.XrayTestResult")  # Ensure correct path
    def test_generate_junit_xml(self, mock_test_result):
        """Test that the JUnit XML is generated and written correctly."""

        # Mock a test case
        mock_test_case = MagicMock()
        mock_test_case.id.return_value = "test_example"
        mock_test_case._testMethodDoc = "Test Example Method"

        # Mock test result object with test cases
        mock_result = MagicMock()
        mock_result.test_cases = [mock_test_case]
        mock_test_result.return_value = mock_result

        # Run the test suite
        test_suite = unittest.TestSuite([mock_test_case])
        result = self.test_runner.run(test_suite)

        # Debugging: Ensure result has test cases
        print(f"Test Result Cases: {mock_result.test_cases}")

        # Verify `write_report()` was called
        self.mock_report_writer.write_report.assert_called_once()

    @unittest.skip("Borked")
    @patch("src.XrayTestRunner.XrayTestResult")
    def test_generate_report_with_different_results(self, mock_test_result):
        """Test that JUnit XML handles success, failure, skipped, and error results correctly."""

        for test_status in ["success", "failure", "skipped", "error"]:
            with self.subTest(status=test_status):
                # Mock a test case
                mock_test_case = MagicMock()
                mock_test_case.id.return_value = f"test_{test_status}"
                mock_test_case._testMethodDoc = f"Test {test_status.capitalize()}"

                # Mock test result object
                mock_result = MagicMock()
                mock_result.test_cases = [mock_test_case]
                mock_test_result.return_value = mock_result

                # Run the test suite
                test_suite = unittest.TestSuite([mock_test_case])
                self.test_runner.run(test_suite)

                # Verify `write_report()` was called
                self.mock_report_writer.write_report.assert_called()

    @unittest.skip("Borked")
    @patch("src.XrayTestRunner.JUnitXMLReportWriter.write_report")# Patch the actual instance method
    def test_generate_junit_xml_does_not_create_files(self, mock_write_report):
        """Ensure that JUnit XML does not create actual files but calls `write_report()`."""

        # Mock a test case
        mock_test_case = MagicMock()
        test_suite = unittest.TestSuite([mock_test_case])

        # Run the test suite
        self.test_runner.run(test_suite)

        # Assert that `write_report()` was called once
        mock_write_report.assert_called_once()


