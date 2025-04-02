from XrayTestRunner import LocalFileStorage, XrayTestRunnerFile
import json
import re

def log_iteration_result(location:str, iteration:int, custom:str=""):
	def decorator(func):
		def wrapper(self, *args, **kwargs):
			storagePlan=LocalFileStorage()
			xtrf=XrayTestRunnerFile(storage=storagePlan)
			try:
				func(self, *args, **kwargs)
			except AssertionError as ae:
				raise ae
			finally:
				xtrf.save(
					name=f"{getattr(self,'_testMethodDoc').strip().split('\n')[0]} iteration {iteration+1} {custom}.json",
					location=location,
					data=json.dumps([self.input_request, self.output], indent=4)
				)
		return wrapper
	return decorator

def set_value(data: dict, key: str, val: any, default: dict | list={}):
	try:
		val=json.loads(val)
	except:
		val=val

	if '.' in key:
		f1, f2 = key.split('.', 1)  # Split only once
		match = re.match(r'(\d+)\.(\w+)', f2)  # Check if f1 contains list indexing
		
		if match:
			index, list_value = match.groups()
			index = int(index)
			
			data[f1][index][list_value] = val  # Modify the existing dict inside list
		else:
			match default:
				case {}:
					data.setdefault(f1, {})[f2] = val
				case []:
					data.setdefault(f1, []).push(val)

	else:
		data[key] = val
