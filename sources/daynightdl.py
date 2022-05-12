"""
Projet DayNightDL

Librairie générale pour le projet DayNightDL
"""

import glob
import os
import sys

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
velocity = None
MIN_VELOCITY = 0.01

VEHICLE_ID = ["a2", "impala", "c3", "microlino", "charger_police", "tt", "wrangler_rubicon", "coupe", "coupe_2020", "low_rider", "charger_2020", "ambulance", "mkz_2020", "mini", "prius", "crown", "carlacola", "zx125", "nissan",
              "charger_police_2020", "sprinter", "etron", "leon", "t2_2021", "cybertruck", "mkz_2017", "mustang", "carlamotors", "volkswagen", "tesla", "century", "omafiets", "grandtourer", "crossbike", "ninja", "yzf", "patrol", "micra", "cooper_s"]


class CamSettings(object):
    def __init__(self, id="a", x=2.5, y=0, z=0.7, roll=0, pitch=0, yaw=0):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getRoll(self):
        return self.roll

    def getPitch(self):
        return self.pitch

    def getYaw(self):
        return self.yaw


def camera_init(tag, world, vehicle, queue, cam_settings, config):
    # config the blueprint
    blueprint_lib = world.get_blueprint_library()
    if tag == "seg":
        camera_bp = blueprint_lib.find("sensor.camera.semantic_segmentation")
    elif tag == "rgb":
        camera_bp = blueprint_lib.find("sensor.camera.rgb")
        camera_bp.set_attribute("motion_blur_intensity", "0")  # 0 => disabled
    else:
        return None

    camera_bp.set_attribute("image_size_x", f"{config.getDimension()[0]}")
    camera_bp.set_attribute("image_size_y", f"{config.getDimension()[1]}")
    camera_bp.set_attribute("sensor_tick", "1")
    camera_bp.set_attribute("fov", f"{config.getFov()}")

    # pick and place
    spawn_point = carla.Transform(carla.Location(
                                                    x=cam_settings.getX(),
                                                    y=cam_settings.getY(),
                                                    z=cam_settings.getZ()
                                                ),
                                  carla.Rotation(
                                                    roll=cam_settings.getRoll(),
                                                    pitch=cam_settings.getPitch(),
                                                    yaw=cam_settings.getYaw()
                                                )
                                  )
    camera = world.spawn_actor(camera_bp, spawn_point, attach_to=vehicle)

    # camera action defined by the sensor callback
    camera.listen(lambda data: sensor_callback(data, queue, config.getTown(), config.getDbname(), tag, cam_settings.getId()))

    return camera


def sensor_callback(image, semaphore, town, dbname, tag, id):
    path = f"../{dbname}/{IMAGE_FOLDER}/{tag}/{town}_{id}_{frame_id}.png"

    if velocity >= MIN_VELOCITY:
        if tag == "seg":
            image.save_to_disk(path, carla.ColorConverter.CityScapesPalette)
        else:
            image.save_to_disk(path)

        semaphore.put((image.frame, image))


def set_weather(world, config):
    weather = carla.WeatherParameters(sun_altitude_angle=config.getAngle())
    world.set_weather(weather)


def set_autonom_car(world, config, traffic_manager, tm_port):
    # config the blueprint
    blueprint_library = world.get_blueprint_library()

    # select enought spawn points
    spawn_list = world.get_map().get_spawn_points()
    nb_vehicle = round(config.getTraffic() / 100 * (len(spawn_list)-1)) + 1
    spawn_list = spawn_list[0:nb_vehicle]

    vehicle_list = [0] * nb_vehicle

    if IMAGE_FOLDER == "NIGHT":
        lights = carla.VehicleLightState.All
    else:
        lights = carla.VehicleLightState.NONE

    max_speed = 100 - config.getSpeed()
    i = 0
    nb_model = len(VEHICLE_ID)
    for spawn in spawn_list:
        id = VEHICLE_ID[i % nb_model]
        vehicle_bp = blueprint_library.filter(id)[0]
        vehicle = world.spawn_actor(vehicle_bp, spawn)
        vehicle.set_light_state(lights)
        vehicle.set_autopilot(True, tm_port)
        traffic_manager.vehicle_percentage_speed_difference(vehicle, max_speed)
        vehicle_list[i] = vehicle
        i += 1

    return vehicle_list


def destroy_carla_object(vehicles, sensors):
    for sensor in sensors:
        sensor.stop()
        sensor.destroy()
    for vehicle in vehicles:
        try:
            vehicle.destroy()
        except RuntimeError:  # vehicle already destroyed
            pass
