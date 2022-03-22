"""
Projet DayNightDL

Librairie générale pour le projet DayNightDL
"""

import glob
import os
import sys
import random

try:
    sys.path.append(
        glob.glob(
            "../carla/dist/carla-*%d.%d-%s.egg"
            % (
                sys.version_info.major,
                sys.version_info.minor,
                "win-amd64" if os.name == "nt" else "linux-x86_64",
            )
        )[0]
    )
except IndexError:
    pass
import carla

import config as conf

IMAGE_FOLDER = "DAY"
frame_id = -1

def camera_init(bp_ref, tag, world, vehicle, queue, confObj):
    """
        Initialisation d'une caméra à partir d'un blueprint.
        Les images sont enregistrées sous _out/ au format frame_tag.png
    """
    # config the blueprint
    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find(bp_ref)
    camera_bp.set_attribute("image_size_x", f"{confObj.width}")
    camera_bp.set_attribute("image_size_y", f"{confObj.height}")
    camera_bp.set_attribute("sensor_tick", "1")
    camera_bp.set_attribute("fov", f"{confObj.fov}")

    # pick and place
    spawn_point = carla.Transform(carla.Location(x=2.5, y=0, z=0.7),
                                  carla.Rotation(roll=0, pitch=0, yaw=0))
    camera = world.spawn_actor(camera_bp, spawn_point, attach_to=vehicle)

    # camera action defined by the sensor callback
    camera.listen(lambda data: sensor_callback(data, queue, tag))

    return camera


def sensor_callback(image, sensor_queue, image_tag):
    """
        Actions exécutées par les caméras à chaque fois qu'une image est reçue
    """
    if image_tag == conf.SEG_TAG:
        image.save_to_disk(f"../DB_{conf.IM_NUMBER}/{IMAGE_FOLDER}/{image_tag}/{frame_id}.png", carla.ColorConverter.CityScapesPalette)
    else:
        image.save_to_disk(f"../DB_{conf.IM_NUMBER}/{IMAGE_FOLDER}/{image_tag}/{frame_id}.png")

    sensor_queue.put((image.frame, image))


def set_weather(world, is_sun):
    """
        Active le jour ou la nuit suivant la valeur du booléen is_sun
    """
    angle = conf.ANGLE_DAY if is_sun else conf.ANGLE_NIGHT

    weather = carla.WeatherParameters(
        cloudiness=0, precipitation=0, sun_altitude_angle=angle
    )
    world.set_weather(weather)


def set_autonom_car(world, traffic_rate, tm_port):
    """
        Met en place un ensemble de véhicules autonomes sur le serveur world
        traffic_rate spécifie le taux de la carte par des voitures
    """
    # config the blueprint
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter("model3")[0]

    # select enought spawn points
    spawn_list = world.get_map().get_spawn_points()
    nb_vehicle = round(traffic_rate / 100 * (len(spawn_list)-1)) + 1
    spawn_list = spawn_list[0:nb_vehicle]

    vehicle_list = []

    if IMAGE_FOLDER == "NIGHT":
        lights = carla.VehicleLightState.All
    else:
        lights = carla.VehicleLightState.NONE

    for spawn in spawn_list:
        vehicle = world.spawn_actor(vehicle_bp, spawn)
        vehicle.set_light_state(lights)
        vehicle.set_autopilot(True, tm_port)
        vehicle_list.append(vehicle)

    return vehicle_list
