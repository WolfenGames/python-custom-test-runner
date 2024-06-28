import unittest
import datetime
from junit_xml import TestSuite
from XrayTestRunner.XrayTestResult import XrayTestResult
import os

class XrayTestRunner(unittest.TextTestRunner):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.resultclass=XrayTestResult
		self.file_path=kwargs.get('file_path', './tests/')
	
	def run(self, test: unittest.TestSuite, **kwargs):
		result=super().run(test, **kwargs)
		self._generate_junit_xml(result)
		return result
	
	def _generate_junit_xml(self, result):
		ts = TestSuite("unittest results", result.test_cases)
		timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

		try:
			os.makedirs(self.file_path)
		except FileExistsError:
			pass

		file_name = f"{self.file_path}/junit_result_{timestamp}.xml"
		try:
			with open(file_name, 'x') as f:
				TestSuite.to_file(f, [ts], prettyprint=True)
		except FileExistsError:
			with open(file_name, 'w') as f:
				TestSuite.to_file(f, [ts], prettyprint=True)
		print(f"\nJUnit XML report generated: {file_name}")
