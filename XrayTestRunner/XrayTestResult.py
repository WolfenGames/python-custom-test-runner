from typing import TextIO
import unittest
from junit_xml import TestCase

class XrayTestResult(unittest.TextTestResult):
	
	def __init__(self, stream: TextIO, descriptions: bool, verbosity: int) -> None:
		super().__init__(stream, descriptions, verbosity)
		self.test_cases=[]

	def addSuccess(self, test: unittest.TestCase) -> None:
		super().addSuccess(test)
		# get the output of the test
		self.test_cases.append(self._create_test_case(test, "success"))

	def addError(self, test: unittest.TestCase, err: tuple) -> None:
		super().addError(test, err)
		self.test_cases.append(self._create_test_case(test, "error"))

	def addFailure(self, test: unittest.TestCase, err: tuple) -> None:
		super().addFailure(test, err)
		self.test_cases.append(self._create_test_case(test, "failed"))

	def addSkip(self, test: unittest.TestCase, reason: str) -> None:
		super().addSkip(test, reason)
		self.test_cases.append(self._create_test_case(test, "skipped"))

	def _create_test_case(self, test: unittest.TestCase, status: str) -> None:
		test_id=test.id().split('.')
		test_name=test_id[-1]

		# get first line from the docstring of the test
		docstring=test._testMethodDoc
		if docstring:
			docstring=docstring.strip().split('\n')[0]
		else:
			docstring=test_name

		try: 
			return TestCase(name=docstring, status=status, stdout=test.output)
		except AttributeError:
			return TestCase(name=docstring, status=status)
