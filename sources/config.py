"""
Projet DayNightDL

Objet de configuration de la simulation

"""

import error as error
import json as JSON

HOST = "localhost"
PORT = 2000

DBNAME = "DB_test"
TOWN_ID = 8

IM_FOV = 110  # field of view
IM_WIDTH = 1920  # in pixels
IM_HEIGHT = 1080  # in pixels
IM_NUMBER = 100  # number of scenes to generate

ANGLE_DAY = 70
ANGLE_NIGHT = -179
TRAFFIC = 10

POSITION = [2.5, 0, 0.7]
ROTATION = [0, 0, 0]

TAG = "a"

SIM_ID = 0

SPEED = 100  # max speed (from 0 to 100)


class Config:

	rgbTag = "rgb"
	segTag = "seg"

	towns = ['town01', 'town02', 'town03', 'town04',
                 'town05', 'town06', 'town07', 'town10HD']

	VEHICLE_ID = ["a2", "impala", "c3", "microlino", "charger_police", "tt", "wrangler_rubicon", "coupe", "coupe_2020", "low_rider", "charger_2020", "ambulance", "mkz_2020", "mini", "prius", "crown", "carlacola", "zx125", "nissan", "charger_police_2020", "sprinter", "etron", "leon", "t2_2021", "cybertruck", "mkz_2017", "mustang", "carlamotors", "volkswagen", "tesla", "century", "omafiets", "grandtourer", "crossbike", "ninja", "yzf", "patrol", "micra", "cooper_s"]

	def __init__(self, host=HOST, port=PORT, dbname=DBNAME, sim=SIM_ID, town=TOWN_ID, fov=IM_FOV, width=IM_WIDTH, height=IM_HEIGHT, imNum=IM_NUMBER, tag=TAG, angle=ANGLE_DAY, traffic=TRAFFIC, position=POSITION, rotation=ROTATION, vehicle_id=VEHICLE_ID, speed=SPEED):
		self.host = host
		self.port = port
		self.sim = sim
		# self.town = Config.towns[int(town)-1]
		self.town = town
		self.fov = int(fov)
		self.width = int(width)
		self.height = int(height)
		self.dimension = [width, height]
		self.imNum = int(imNum)
		self.tag = tag
		self.angle = int(angle)
		self.traffic = int(traffic)
		self.vehicle_id = vehicle_id
		self.speed = 100
		self.fps = 1
		self.position = position
		self.rotation = rotation
		self.dbname = dbname

	def getHost(self):
		return self.host

	def getPort(self):
		return int(self.port)

	def getTown(self):
		return self.town

	def getFov(self):
		return self.fov

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getImNum(self):
		return self.imNum

	def getTag(self):
		return self.tag

	def getPosition(self):
		return self.position

	def getRotation(self):
		return self.rotation

	def getAngle(self):
		return int(self.angle)

	def getTraffic(self):
		return self.traffic

	def getVehicleId(self):
		return self.vehicle_id

	def checkConfig(self):
		error.checkConnection(self.host, self.port)
		error.checkDimensions(self.width, self.height)
		error.checkFov(self.fov)
		error.checkImgNum(self.imNum)

	def __str__(self) -> str:
		ret_str = "Conf object\n"
		for a in dir(self):
			ret_str += "{} : {}\n".format(a, type(getattr(self, a)))
		return ret_str

def confFromJSON(json : JSON):
	decoded = json

	confDay = Config(decoded['host'], decoded['port'], DBNAME, SIM_ID , decoded['town'], decoded['fov'],
	decoded['width'], decoded['height'], decoded['imNum'], TAG, decoded['day'],
	decoded['traffic'], POSITION, ROTATION, Config.VEHICLE_ID)

	confNight = Config(decoded['host'], decoded['port'],DBNAME, SIM_ID , decoded['town'], decoded['fov'],
	decoded['width'], decoded['height'], decoded['imNum'], TAG, decoded['night'],
	decoded['traffic'], POSITION, ROTATION, Config.VEHICLE_ID)
	return (confDay, confNight)

globalConf = Config(HOST, PORT, DBNAME, SIM_ID, TOWN_ID, IM_FOV, IM_WIDTH, IM_HEIGHT, IM_NUMBER, TAG,
					ANGLE_DAY, TRAFFIC, POSITION, ROTATION, Config.VEHICLE_ID, SPEED)
