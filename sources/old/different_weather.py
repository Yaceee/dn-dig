import daynightdl as dn
import config as conf
from tqdm import tqdm

from queue import Queue, Empty
from time import sleep


def simulation(confObj):
    try:
        # ---------------------------------------------------------------------
        # INITIALIZATION
        #
        # client
        client = dn.carla.Client(confObj.host, confObj.port)
        client.set_timeout(10.0)

        # load the specified world
        try:
            world = client.load_world(conf.TOWN_ID)
        except RuntimeError:
            print(f"{conf.TOWN_ID} not found, use the current world")
            world = client.get_world()

        # set world mode to synchronous
        world.apply_settings(
                dn.carla.WorldSettings(synchronous_mode=True,
                                       no_rendering_mode=False,
                                       fixed_delta_seconds=0.05))

        # weather
        dn.IMAGE_FOLDER = "WEATHER"

        # car configuration
        sensor_queue = Queue()
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter("model3")[0]

        # pick and place
        spawn_point = world.get_map().get_spawn_points()[1]
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        cam_rgb = dn.camera_init(
            "sensor.camera.rgb", confObj.rgbTag, world, vehicle, sensor_queue, confObj
        )

        # ---------------------------------------------------------------------
        # SIMULATION
        #
        world.tick()
        print(f"Recording {dn.IMAGE_FOLDER} images")
        for dn.frame_id in tqdm(range(-180, 180)):
            try:
                sensor_queue.get(block=True, timeout=2)
            except Empty:
                continue

            weather = dn.carla.WeatherParameters(
                cloudiness=0, precipitation=0, sun_altitude_angle=dn.frame_id
            )
            world.set_weather(weather)

            for _ in range(20):
                world.tick()
        #
        # ---------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # CLEANING
    #
    finally:
        world.apply_settings(dn.carla.WorldSettings(False, False, 0))
        vehicle.destroy()
        cam_rgb.stop()
        cam_rgb.destroy()
        print("Server cleaned")


if __name__ == '__main__':
    simulation(confObj=conf.globalConf)
    sleep(2) # allow time for saving the last image
