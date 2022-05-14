from threading import Thread
from time import sleep
from copy import deepcopy
import os
import json

from simulation import simulation
from config import Config


class SimThread(Thread):
    def __init__(self, config: Config):
        self.conf = config
        Thread.__init__(self)

    def run(self):
        simulation(self.conf)


def record(input):
    if(type(input) == str):
        with open(input) as jsonFile:
            globalData = json.load(jsonFile)
    else:
        globalData = input
        globalData["angle"] = [globalData["day"], globalData["night"]]
        globalData["dimension"] = [globalData["width"], globalData["height"]]
        globalData["speed"] = 100
        print(globalData)

    for town in globalData["town"]:
        for angle in globalData["angle"]:
            os.system(f"gnome-terminal --tab --title \"Server on {town}\" -- /opt/carla-simulator/CarlaUE4.sh -opengl -RenderOffScreen")

            data = deepcopy(globalData)
            data["town"] = town
            data["angle"] = angle
            configObject = Config(data)

            sleep(2)
            thread = SimThread(configObject)
            thread.start()
            thread.join()

            carlaPID = os.popen("ps -a | grep Carla | awk '{print $1}'").read()[:-1]
            os.kill(int(carlaPID), 9)


if __name__ == "__main__":
    record("./conf.json")
