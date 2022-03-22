import error

HOST = "localhost"
PORT = 2000

TOWN_ID = "town01"

IM_FOV = 110  # field of view
IM_WIDTH = 640  # in pixels
IM_HEIGHT = 480  # in pixels
IM_NUMBER = 10  # number of scenes to generate

ANGLE_DAY = 70
ANGLE_NIGHT = -178
TRAFFIC_PERCENTAGE = 20

RGB_TAG = "rgb"
SEG_TAG = "seg"

TM_PORT = 8000 # must be different than PORT
TM_SEED = 1 # traffic manager seed


class Config:

    rgbTag = "rgb"
    segTag = "seg"

    

    def __init__(self, host, port, fov, width, height, imNum):
        self.host = host
        self.port = port
        self.fov = fov
        self.width = width
        self.height = height
        self.imNum = imNum

    def checkConfig(self):
        error.checkConnection(self.host, self.port)
        error.checkDimensions(self.width, self.height)
        error.checkFov(self.fov)
        error.checkImgNum(self.imNum)

globalConf = Config(HOST, PORT, IM_FOV, IM_WIDTH, IM_HEIGHT, IM_NUMBER)
