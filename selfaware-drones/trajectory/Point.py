import matplotlib.pyplot as plt

class Point:
	'''
	To represent a point in R^N
	'''
	def __init__(self,cords=[]):
		self._cords=cords

	def getCords(self):
		return self._cords

	def getStrCords(self, delim=",", end=""):
		cordStr = ""
		cordStr += delim.join([str(i) for i in self.getCords()])
		if(end != ""):
			cordStr += end
		return cordStr


	def echo(self):
		print(self._cords)

	def getDim(self)->int:
		return len(self._cords)

class Points:
	'''
	To represent many points in of same dimension
	'''
	def __init__(self):
		self._pointsList = []

	def getPointsList(self)->list:
		return self._pointsList

	def getDim(self)->int:
		return len(self._pointsList[0].getCords())

	def add(self,point:Point):
		self.getPointsList().append(point)

	def getLen(self)->int:
		return len(self._pointsList)

	def getDimAggregatedPoints(self)->list:
		dimAggregated = []
		for point in self._pointsList:
			dimCtr = 0
			while (dimCtr < self.getDim()):
				if(len(dimAggregated)<=dimCtr):
					dimAggregated.append([])
				dimAggregated[dimCtr].append(point.getCords()[dimCtr])
				dimCtr+=1
		return dimAggregated

	def echo(self):
		for p in self.getPointsList():
			print(p.getCords())

	def addDim(self, defaultVal):
		newPointsList = []
		for point in self.getPointsList():
			point.getCords().append(defaultVal)
			newPointsList.append(point)
		self._pointsList=newPointsList

	def echoFile(self, path, hDelim=",", vDelim="\n"):
		f = open(path, "w")
		str = ""
		for point in self.getPointsList():
			str += point.getStrCords(" ",vDelim)
		f.write(str)





	def plot3DPoints(self):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		x = self.getDimAggregatedPoints()[0]
		y = self.getDimAggregatedPoints()[1]
		z = self.getDimAggregatedPoints()[2]
		ax.scatter(x, y, z, c='r', marker='o')
		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')
		plt.show()