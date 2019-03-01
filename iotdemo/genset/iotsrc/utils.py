class Utilities:
	def __init__(self):
		pass
	def parse_bin(self,s):
		t = s.split('.')
		return int(t[0], 2) + int(t[1], 2) / 2.**len(t[1])
	def result_energy(self, f_num, l_num):
		f_num = '{0:016b}'.format(f_num)
		l_num = '{0:016b}'.format(l_num)
		val="".join((f_num,l_num))
		S=int(val[0])
		E=val[1:9]
		E10= int(E,2)
		D=val[9:]
		y_=".".join(("1",D))
		y=self.parse_bin(y_)
		result = (pow(-1,S))*(pow(2,(E10-127)))*y
		return round(result,2)

'''if __name__ == "__main__":
	obj = Utilities()
	data = obj.result_energy(17264,28705)
	print(data)	'''
