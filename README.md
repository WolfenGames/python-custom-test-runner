# XrayTestRunner

Purpose of this package is to be able to export tests run with output to a file.

The idea is read this file into xray to update the status of a test run with ease.

## Example in code
```python
....
from XrayTestRunner import XrayTestRunner

class SomeTest(unittest.TestCase):
	....
	....

if __name__ == "__main__":
	unittest.main(testRunner=XrayTestRunner())

```
