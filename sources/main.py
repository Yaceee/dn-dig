"""
Equivalent de main.sh en python, ne pas hésiter à modifier / reprendre
"""
from time import sleep
import os


def record():
    config = {
        "host": "localhost",
        "port": "2000",
        "dbname": "DB_",
        "town": ["town01", "town02"],
        "dimension": ["1920", "1080"],
        "imNum": "3",
        "traffic": "15",
        "fov": "110",
        "seed": "1",
        "speed": "100",
        "angle": ["70", "-165"]
    }
    arg = ""
    for key, val in config.items():
        arg += " --" + key + " "
        if key == "angle" or key == "town":
            arg += "{" + key + "}"
        elif key == "dimension":
            arg += val[0] + " " + val[1]
        else:
            arg += val

    for town in config["town"]:
        for angle in config["angle"]:
            os.system(f"gnome-terminal --tab --title \"Server on {town}\" -- /opt/carla-simulator/CarlaUE4.sh -opengl -RenderOffScreen")
            sleep(2)
            try:
                os.system("python3 simulation.py" + arg.format(town=town, angle=angle))
            except:
                pass

            carlaPID = os.popen("ps -a | grep Carla | awk '{print $1}'").read()[:-1]
            os.kill(int(carlaPID), 9)


record()
