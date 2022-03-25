"""
Projet DayNightDL

Objet de configuration de la simulation

"""

import sources.error as error

HOST = "localhost"
PORT = 2000

TOWN_ID = "town01"

IM_FOV = 110  # field of view
IM_WIDTH = 640  # in pixels
IM_HEIGHT = 480  # in pixels
IM_NUMBER = 50  # number of scenes to generate

ANGLE_DAY = 70
ANGLE_NIGHT = -178
TRAFFIC = 20

VEHICLE_ID = ["a2", "impala", "c3", "microlino", "charger_police", "tt", "wrangler_rubicon", "coupe", "coupe_2020", "low_rider", "charger_2020", "ambulance", "mkz_2020", "mini", "prius", "crown", "carlacola", "zx125", "nissan", "charger_police_2020", "sprinter", "etron", "leon", "t2_2021", "cybertruck", "mkz_2017", "mustang", "carlamotors", "volkswagen", "tesla", "century", "omafiets", "grandtourer", "crossbike", "ninja", "yzf", "patrol", "micra", "cooper_s"]

class Config:

    rgbTag = "rgb"
    segTag = "seg"


    def __init__(self, host, port, town, fov, width, height, imNum, sun, moon, traffic, vehicle_id):
        self.host = host
        self.port = port
        self.town = town
        self.fov = fov
        self.width = width
        self.height = height
        self.imNum = imNum
        self.sun = sun
        self.moon = moon
        self.traffic = traffic
        self.vehicle_id = vehicle_id

    def checkConfig(self):
        error.checkConnection(self.host, self.port)
        error.checkDimensions(self.width, self.height)
        error.checkFov(self.fov)
        error.checkImgNum(self.imNum)

globalConf = Config(HOST, PORT, TOWN_ID, IM_FOV, IM_WIDTH, IM_HEIGHT, IM_NUMBER,
                    ANGLE_DAY, ANGLE_NIGHT, TRAFFIC, VEHICLE_ID)
