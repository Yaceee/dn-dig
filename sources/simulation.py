import daynightdl as dn
import argparse
import numpy as np

from config import Config
from tqdm import tqdm
from queue import Queue, Empty
from time import sleep


def simulation(config: Config, seed: int):
    # ---------------------------------------------------------------------
    # INITIALIZATION
    #
    # client
    client = dn.carla.Client(config.getHost(), config.getPort())
    client.set_timeout(10.0)

    pbar = tqdm(total=config.imNum)  # progression bar displayed
    for town in config.towns:
        # load the specified world
        try:
            world = client.load_world(town)
        except RuntimeError:
            print(f"Can not load {town} on the server, try next one")
            continue

        # set world mode to synchronous
        delta_sec = 0.1  # delta_sec <= 0.1 (github issue #695)
        world.apply_settings(dn.carla.WorldSettings(
                                synchronous_mode=True,
                                no_rendering_mode=False,
                                fixed_delta_seconds=delta_sec)
                             )

        # Set up the traffic manager
        TM_PORT = 8000
        try:
            traffic_manager = client.get_trafficmanager(TM_PORT)
        except RuntimeError:
            TM_PORT += 1
            traffic_manager = client.get_trafficmanager(TM_PORT)
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(seed)

        # weather
        dn.IMAGE_FOLDER = "DAY" if config.angle >= 0 else "NIGHT"
        dn.set_weather(world, config)

        # set traffic and pick the first car
        vehicle_list = dn.set_autonom_car(
            world, config, traffic_manager, TM_PORT)
        vehicle = vehicle_list[0]
        traffic_manager.ignore_lights_percentage(vehicle, 100)

        # attach cameras to the vehicle
        sensor_list = []
        semaphore = Queue()

        sensor_settings = [dn.CamSettings(id="f"),
                           dn.CamSettings(id="h", x=5, z=10, pitch=-40),
                           dn.CamSettings(id="r", y=5, x=4, z=2, yaw=90),
                           dn.CamSettings(id="l", y=-8,x=4, z=2, yaw=-90)]

        for setting in sensor_settings:
            cam_rgb = dn.camera_init("rgb", world, town, vehicle, semaphore,
                                     setting, config)
            cam_seg = dn.camera_init("seg", world, town, vehicle, semaphore,
                                     setting, config)

            sensor_list.append(cam_rgb)
            sensor_list.append(cam_seg)

        # -----------------------------------------------------------------
        # SIMULATION
        #
        world.tick()
        dn.frame_id = 1
        pbar.set_description(town)
        pbar.reset()
        while dn.frame_id < config.imNum+1:
            dn.velocity = vehicle.get_velocity().length()
            # Save images (need dn.velocity updated before)
            try:
                for _ in range(len(sensor_list)):
                    semaphore.get(block=True, timeout=5)
            except Empty:
                print("Sensor error")
                continue

            # Update progress bar
            if dn.velocity > dn.MIN_VELOCITY:
                dn.frame_id += 1
                pbar.update()

            # Allow the server to generate the next scene
            [world.tick() for _ in range(round(1/delta_sec))]

        pbar.close()
        #
        # -----------------------------------------------------------------
        sleep(2)  # allow time to save the last image

        # -----------------------------------------------------------------
        # CLEANING
        #
        for sensor in sensor_list:
            sensor.stop()
            sensor.destroy()
        for vehicle in vehicle_list:
            vehicle.destroy()
        world.apply_settings(dn.carla.WorldSettings(False, False, 0))

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '--host',
        default='localhost',
        help='IP of the host server (default: localhost)'
    )
    argparser.add_argument(
        '--port', '-p',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)'
    )
    argparser.add_argument(
        '--dbname', '-n',
        default='DB',
        help='Main folder name where images are stored (default: DB)'
    )
    argparser.add_argument(
        '--tag',
        default='a',
        help='Extra tag for image names (default: a)'
    )
    argparser.add_argument(
        '--town',
        default='1',
        help='Deprecated !'
    )
    argparser.add_argument(
        '--speed', '-s',
        default=100,
        type=float,
        help='Vehicles speed percentage (default: 100 => the fastest)'
    )
    argparser.add_argument(
        '--fps', '-fps',
        default=1,
        type=float,
        help='Number of fps in simulator time (default: 1)'
    )
    argparser.add_argument(
        '--fov',
        default=110,
        type=int,
        help='Field of view (default: 110)'
    )
    argparser.add_argument(
        '--dimension', '-d',
        nargs='+',
        type=int,
        default=[1920, 1080],
        help='Image dimension (default: [1920, 1080])'
    )
    argparser.add_argument(
        '--imNum', '-N',
        default=100,
        type=int,
        help='Number of image (default: 100)'
    )
    argparser.add_argument(
        '--angle', '-a',
        default=70,
        type=float,
        help='Angle between the sun and the ground (default: 70)'
    )
    argparser.add_argument(
        '--traffic', '-tr',
        default=0,
        type=int,
        help='Traffic percentage (default: 0)'
    )
    argparser.add_argument(
        '--position',
        nargs='+',
        type=float,
        default=[2.5, 0, 0.7],
        help='(x,y,z) camera position (default: [2.5, 0, 0.7])'
    )
    argparser.add_argument(
        '--rotation',
        nargs='+',
        type=float,
        default=[0, 0, 0],
        help='(roll,yaw,pitch) camera rotation (default: [0, 0, 0])'
    )
    argparser.add_argument(
        '--seed',
        type=int,
        default=1,
        help='Seed to initialize random sequences'
    )

    config = argparser.parse_args()
    conf_obj = Config(config.host, config.port, config.dbname, config.tag, config.town, config.fov, config.dimension[0], config.dimension[1], config.imNum, config.tag, config.angle, config.traffic, config.position, config.rotation, config.speed)

    simulation(conf_obj, config.seed)

    sleep(2)  # allow time to save the last image
