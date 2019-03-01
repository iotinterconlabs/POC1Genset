import json


class DataOperation:
	def __init__(self):
		pass
	def write_data_in_file(self,data):
		self.data = data
		if type(self.data) == dict:
			with open('/home/ubuntu/iotdemo/genset/datafile/data.json', 'w') as f:
				json.dump(data, f)
				
	def read_data_from_file(self):
		with open('/home/ubuntu/iotdemo/genset/datafile/data.json') as f:
			data = json.load(f)
		return dict(data)
