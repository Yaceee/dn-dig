from threading import Thread
from time import time_ns

import simulation
from config import Config


class SimThread(Thread):
    def __init__(self, config: Config, seed: int):
        self.conf = config
        self.seed = seed
        Thread.__init__(self)

    def run(self):
        simulation.simulation(self.conf, self.seed)


def startSimulationThreads(configDay: Config, configNight: Config):
    seed = time_ns()

    t_day = SimThread(configDay, seed)
    t_night = SimThread(configNight, seed)


    print("start Day Sim")
    t_day.start()
    t_day.join()

    print("start Night Sim")
    t_night.start()
    t_night.join()
