from threading import Thread

import simulation
from config import Config

class SimThread(Thread):
    def __init__(self, config : Config):
        self.conf = config
        Thread.__init__(self)

    def run(self):
        simulation.simulation(self.conf)


def startSimulationThreads(configDay : Config, configNight : Config):
    t_day = SimThread(configDay)
    t_night = SimThread(configNight)

    t_day.start()
    t_night.start()

    t_day.join()
    t_night.join()

