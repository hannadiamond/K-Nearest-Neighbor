class Instance(object):
	def __init__(self, inputList):
		self.inputList = inputList
		self.label = inputList[0]
		self.listString = []
		self.listNum = []

	def process(self):
		iterList = iter(self.inputList)
		next(iterList)
		for item in iterList:
			if item[0] == "\"":
				self.listString.append(item)
			else:
				self.listNum.append(float(item))

			# try:
			# 	float(repr(item))
			# 	self.listNum.append(item)
			# 	print("added")
			# except:
			# 	self.listString.append(item)

	def GetlistNum(self):
		return self.listNum

	def GetlistString(self):
		return self.listString

	def Getlabel(self ):
		return self.label
