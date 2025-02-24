import unittest
import datetime
import os
from typing import Optional, Protocol
from junit_xml import TestSuite
from XrayTestRunner.XrayTestResult import XrayTestResult


class IReportWriter(Protocol):
    """Interface for generating test reports."""
    def write_report(self, test_suite: TestSuite) -> None:
        pass


class JUnitXMLReportWriter(IReportWriter):
    """Generates and writes JUnit XML reports."""
    
    def __init__(self, output_dir: str = "./tests/") -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write_report(self, test_suite: TestSuite) -> None:
        """Writes test results to a JUnit XML file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = os.path.join(self.output_dir, f"junit_result_{timestamp}.xml")

        try:
            print(f"Attempting to write report to: {file_name}")
            with open(file_name, "w") as f:
                TestSuite.to_file(f, [test_suite], prettyprint=True)
            print(f"\nJUnit XML report generated: {file_name}")
        except OSError as e:
            print(f"Error writing JUnit report: {e}")


class XrayTestRunner(unittest.TextTestRunner):
    """Custom test runner supporting JUnit XML reporting."""
    
    def __init__(
        self, 
        report_writer: Optional[IReportWriter] = None, 
        *args, 
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.resultclass = XrayTestResult
        self.report_writer = report_writer or JUnitXMLReportWriter()

    def run(self, test: unittest.TestSuite, **kwargs) -> unittest.TestResult:
        """Runs tests and generates a report."""
        result = super().run(test, **kwargs)
        self._generate_report(result)
        return result

    def _generate_report(self, result: XrayTestResult) -> None:
        """Creates and writes a test report using the configured report writer."""
        test_suite = TestSuite("unittest results", result.test_cases)
        self.report_writer.write_report(test_suite)
