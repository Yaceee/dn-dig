"""
Projet DayNightDL

Objet de configuration de la simulation

"""

import error
import json
from types import SimpleNamespace

class Config:
	def __init__(self, data):
		self.data = data

	def getHost(self):
		return self.data.host

	def getPort(self):
		return int(self.data.port)

	def getDbname(self):
		return self.data.dbname

	def getTown(self):
		return self.data.town

	def getSpeed(self):
		return self.data.speed

	def getFov(self):
		return self.data.fov

	def getDimension(self):
		return self.data.dimension

	def getImNum(self):
		return int(self.data.imNum)

	def getAngle(self):
		return int(self.data.angle)

	def getTraffic(self):
		return int(self.data.traffic)

	def getSeed(self):
		return int(self.data.seed)

	def checkConfig(self):
		return (
			error.checkConnection(self.data.host, self.data.port)
		and error.checkDimensions(self.data.width, self.data.height)
		and error.checkFov(self.data.fov)
		and error.checkImgNum(self.data.imNum)
		and error.checkAngle(self.data.angle)
		and error.checkTown(self.data.town))


	def __str__(self) -> str:
		ret_str = "Conf object\n"
		for a in dir(self):
			ret_str += "{} : {}\n".format(a, type(getattr(self, a)))
		return ret_str

def confFromJSON(data : json):
	decoded = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

	confDay = Config(decoded)

	confNight = Config(decoded)
	return (confDay, confNight)
