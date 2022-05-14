"""
Projet DayNightDL

Objet de configuration de la simulation

"""

import error


class Config(object):
    def __init__(self, data):
        self.host = data["host"]
        self.port = data["port"]
        self.dbname = data["dbname"]
        self.town = data["town"]
        self.dimension = data["dimension"]
        self.imnum = data["imnum"]
        self.traffic = data["traffic"]
        self.fov = data["fov"]
        self.seed = data["seed"]
        self.speed = data["speed"]
        self.angle = data["angle"]

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def getDbname(self):
        return self.dbname

    def getTown(self):
        return self.town

    def getSpeed(self):
        return self.speed

    def getFov(self):
        return self.fov

    def getDimension(self):
        return self.dimension

    def getImNum(self):
        return self.imnum

    def getAngle(self):
        return self.angle

    def getTraffic(self):
        return self.traffic

    def getSeed(self):
        return self.seed

    def checkConfig(self):
        return(
            error.checkConnection(self.host, self.port)
            and error.checkDimensions(self.dimension)
            and error.checkFov(self.fov)
            and error.checkImgNum(self.imnum)
            and error.checkAngle(self.angle)
            and error.checkTown(self.town)
        )

    def print(self):
        print(f"""
        host: {self.getHost()}
        port: {self.getPort()}
        dbname: {self.getDbname()}
        town: {self.getTown()}
        angle: {self.getAngle()}
        imnum: {self.getImNum()}
        dimension: {self.getDimension()}
        fov: {self.getFov()}
        speed: {self.getSpeed()}
        traffic: {self.getTraffic()}
        seed: {self.getSeed()}
        """
              )

    def __str__(self) -> str:
        ret_str = "Conf object"
        for a in dir(self):
            ret_str += "\n{} : {}".format(a, type(getattr(self, a)))
        return ret_str
