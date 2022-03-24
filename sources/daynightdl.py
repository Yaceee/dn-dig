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

IMAGE_FOLDER = None
frame_id = None

def camera_init(tag, world, vehicle, queue, confObj):
    # config the blueprint
    blueprint_library = world.get_blueprint_library()
    if tag == "seg":
        camera_bp = blueprint_library.find("sensor.camera.semantic_segmentation")
    elif tag == "rgb":
        camera_bp = blueprint_library.find("sensor.camera.rgb")
    else:
        return None

    camera_bp.set_attribute("image_size_x", f"{confObj.width}")
    camera_bp.set_attribute("image_size_y", f"{confObj.height}")
    camera_bp.set_attribute("sensor_tick", "1")
    camera_bp.set_attribute("fov", f"{confObj.fov}")

    # pick and place
    spawn_point = carla.Transform(carla.Location(x=2.5, y=0, z=0.7),
                                  carla.Rotation(roll=0, pitch=0, yaw=0))
    camera = world.spawn_actor(camera_bp, spawn_point, attach_to=vehicle)

    # camera action defined by the sensor callback
    camera.listen(lambda data: sensor_callback(data, queue, tag, confObj))

    return camera


def sensor_callback(image, sensor_queue, tag, confObj):
    if tag == confObj.segTag:
        image.save_to_disk(f"../DB_{confObj.imNum}/{IMAGE_FOLDER}/{tag}/{frame_id}.png", carla.ColorConverter.CityScapesPalette)
    else:
        image.save_to_disk(f"../DB_{confObj.imNum}/{IMAGE_FOLDER}/{tag}/{frame_id}.png")

    sensor_queue.put((image.frame, image))


def set_weather(world, is_sun, confObj):
    angle = confObj.sun if is_sun else confObj.moon
    weather = carla.WeatherParameters(sun_altitude_angle=angle)
    world.set_weather(weather)


def set_autonom_car(world, confObj, tm_port):
    # config the blueprint
    blueprint_library = world.get_blueprint_library()

    # select enought spawn points
    spawn_list = world.get_map().get_spawn_points()
    nb_vehicle = round(confObj.traffic / 100 * (len(spawn_list)-1)) + 1
    spawn_list = spawn_list[0:nb_vehicle]

    vehicle_list = [0] * nb_vehicle

    if IMAGE_FOLDER == "NIGHT":
        lights = carla.VehicleLightState.All
    else:
        lights = carla.VehicleLightState.NONE

    i = 0
    nb_model = len(confObj.vehicle_id)
    for spawn in spawn_list:
        id = confObj.vehicle_id[i % nb_model]
        vehicle_bp = blueprint_library.filter(id)[0]
        vehicle = world.spawn_actor(vehicle_bp, spawn)
        vehicle.set_light_state(lights)
        vehicle.set_autopilot(True, tm_port)
        vehicle_list[i] = vehicle
        i += 1

    return vehicle_list
