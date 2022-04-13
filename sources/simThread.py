from threading import Thread

import simulation
from config import Config

def startSimulationThreads(configDay : Config, configNight : Config):
    t_day = Thread(target=simulation.simulation, args=(configDay,))
    t_night = Thread(target=simulation.simulation, args=(configNight,))

    t_day.start()
    t_night.start()

    t_day.join()
    t_night.join()

