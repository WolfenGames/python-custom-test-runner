import os

class XrayTestRunnerFile():
	def Save(name: str, location: str, data: str):
		try:
			os.makedirs(location, exist_ok=True)
		except FileExistsError:
			pass

		with open(f"{location}/{name}", 'w') as f:
			f.write(data)
