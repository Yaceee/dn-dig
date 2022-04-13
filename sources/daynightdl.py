"""
Projet DayNightDL

Librairie générale pour le projet DayNightDL
"""

import glob
import os
import sys

from sources.config import Config

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

IMAGE_FOLDER = None
frame_id = None

VEHICLE_ID = ["a2", "impala", "c3", "microlino", "charger_police", "tt", "wrangler_rubicon", "coupe", "coupe_2020", "low_rider", "charger_2020", "ambulance", "mkz_2020", "mini", "prius", "crown", "carlacola", "zx125", "nissan",
              "charger_police_2020", "sprinter", "etron", "leon", "t2_2021", "cybertruck", "mkz_2017", "mustang", "carlamotors", "volkswagen", "tesla", "century", "omafiets", "grandtourer", "crossbike", "ninja", "yzf", "patrol", "micra", "cooper_s"]


def camera_init(tag, world, vehicle, queue, config):
    # config the blueprint
    blueprint_lib = world.get_blueprint_library()
    if tag == "seg":
        camera_bp = blueprint_lib.find("sensor.camera.semantic_segmentation")
    elif tag == "rgb":
        camera_bp = blueprint_lib.find("sensor.camera.rgb")
    else:
        return None

    camera_bp.set_attribute("image_size_x", f"{config.dimension[0]}")
    camera_bp.set_attribute("image_size_y", f"{config.dimension[1]}")
    camera_bp.set_attribute("sensor_tick", f"{config.fps}")
    camera_bp.set_attribute("fov", f"{config.fov}")

    # pick and place
    spawn_point = carla.Transform(carla.Location(
                                                    x=config.position[0],
                                                    y=config.position[1],
                                                    z=config.position[2]
                                                ),
                                  carla.Rotation(
                                                    roll=config.rotation[0],
                                                    pitch=config.rotation[1],
                                                    yaw=config.rotation[2]
                                                )
                                  )
    camera = world.spawn_actor(camera_bp, spawn_point, attach_to=vehicle)

    # camera action defined by the sensor callback
    camera.listen(lambda data: sensor_callback(data, queue, tag, config))

    return camera


def sensor_callback(image, sensor_queue, tag, config):
    path = f"../{config.dbname}/{IMAGE_FOLDER}/{tag}/{config.town}_{config.tag}_{frame_id}.png"
    if tag == "seg":
        image.save_to_disk(path, carla.ColorConverter.CityScapesPalette)
    else:
        image.save_to_disk(path)

    sensor_queue.put((image.frame, image))


def set_weather(world, config):
    weather = carla.WeatherParameters(sun_altitude_angle=config.angle)
    world.set_weather(weather)


def set_autonom_car(world, config : Config, tm_port):
    # config the blueprint
    blueprint_library = world.get_blueprint_library()

    # select enought spawn points
    spawn_list = world.get_map().get_spawn_points()
    nb_vehicle = round(config.traffic / 100 * (len(spawn_list)-1)) + 1
    spawn_list = spawn_list[0:nb_vehicle]

    vehicle_list = [0] * nb_vehicle

    if IMAGE_FOLDER == "NIGHT":
        lights = carla.VehicleLightState.All
    else:
        lights = carla.VehicleLightState.NONE

    max_speed = 100 - config.speed
    i = 0
    nb_model = len(config.getVehicleId())
    for spawn in spawn_list:
        id = config.getVehicleId()[i % nb_model]
        vehicle_bp = blueprint_library.filter(id)[0]
        vehicle = world.spawn_actor(vehicle_bp, spawn)
        vehicle.set_light_state(lights)
        vehicle.set_autopilot(True, tm_port)
        traffic_manager.vehicle_percentage_speed_difference(vehicle, max_speed)
        vehicle_list[i] = vehicle
        i += 1

    return vehicle_list
