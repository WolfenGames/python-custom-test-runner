from typing import TextIO, List, Tuple, Dict, Optional, Protocol
import unittest
from junit_xml import TestCase
import os
import json


class ITestResultProcessor(Protocol):
    """Abstract interface for processing test results."""
    def process(self, test_case: TestCase) -> None:
        pass


class JSONTestResultProcessor(ITestResultProcessor):
    """Processes test results by writing them to JSON files."""
    
    def __init__(self, output_dir: str = "./tests/output") -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def process(self, test_case: TestCase) -> None:
        """Writes test result data to a JSON file."""
        file_path = os.path.join(self.output_dir, f"{test_case.name}.json")
        with open(file_path, "w") as f:
            f.write(json.dumps(test_case.stdout, indent=4))


class XrayTestResult(unittest.TextTestResult):
    """Custom test result class that supports processing test results."""

    def __init__(
        self, 
        stream: TextIO, 
        descriptions: bool, 
        verbosity: int, 
        processor: Optional[ITestResultProcessor] = None
    ) -> None:
        super().__init__(stream, descriptions, verbosity)
        self.test_cases: List[TestCase] = []
        self.processor = processor or JSONTestResultProcessor()

    def addSuccess(self, test: unittest.TestCase) -> None:
        super().addSuccess(test)
        self._handle_result(test, "success")

    def addError(self, test: unittest.TestCase, err: Tuple) -> None:
        super().addError(test, err)
        self._handle_result(test, "error")

    def addFailure(self, test: unittest.TestCase, err: Tuple) -> None:
        super().addFailure(test, err)
        self._handle_result(test, "failed")

    def addSkip(self, test: unittest.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
        self._handle_result(test, "skipped")

    def _handle_result(self, test: unittest.TestCase, status: str) -> None:
        """Creates and processes a test case result."""
        test_case = self._create_test_case(test, status)
        self.test_cases.append(test_case)
        self.processor.process(test_case)

    def _create_test_case(self, test: unittest.TestCase, status: str) -> TestCase:
        """Creates a test case object with structured data."""
        test_id = test.id().split('.')
        test_name = test_id[-1]

        # Get first line of docstring if available
        docstring = test._testMethodDoc
        docstring = docstring.strip().split("\n")[0] if docstring else test_name

        stdout = self._extract_test_data(test)

        return TestCase(name=docstring, status=status, stdout=stdout)

    def _extract_test_data(self, test: unittest.TestCase) -> List[Dict]:
        """Extracts input and output data from a test case."""
        stdout = []

        if hasattr(test, "inputRequest"):
            stdout.append({"inputRequest": test.inputRequest})

            
        if hasattr(test, "input_request"):
            stdout.append({"input_request": test.input_request})

        if hasattr(test, "output"):
            stdout.append({"output": test.output})

        return stdout
