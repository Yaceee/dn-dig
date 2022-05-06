import daynightdl as dn
import argparse
import numpy as np
import sys

from config import Config
from tqdm import tqdm
from queue import Queue, Empty
from time import sleep


def simulation(config: Config):
    # -------------------------------------------------------------------------
    # INITIALIZATION
    #
    vehicle_list = []
    sensor_list = []
    pbar = tqdm(total=config.getImNum())  # progression bar displayed

    try:
        # get the client
        client = dn.carla.Client(config.getHost(), config.getPort())
        client.set_timeout(10.0)

        # set up the server world
        try:
            pbar.set_description("init...")
            pbar.reset()
            delta_sec = 0.1  # delta_sec <= 0.1 (github issue #695)
            world = client.get_world()
            world = client.load_world(config.getTown())
            world.apply_settings(dn.carla.WorldSettings(True, False, delta_sec))
        except RuntimeError:
            pbar.set_description(f"Can not load {config.getTown()} on the server")
            pbar.close()
            sys.exit(1)

        # Set up the traffic manager
        TM_PORT = 8000
        try:
            traffic_manager = client.get_trafficmanager(TM_PORT)
        except RuntimeError:
            TM_PORT += 1
            traffic_manager = client.get_trafficmanager(TM_PORT)
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(config.getSeed())

        # weather
        dn.IMAGE_FOLDER = "DAY" if config.getAngle() >= 0 else "NIGHT"
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
            cam_rgb = dn.camera_init("rgb", world, vehicle, semaphore,
                                     setting, config)
            cam_seg = dn.camera_init("seg", world, vehicle, semaphore,
                                     setting, config)

            sensor_list.append(cam_rgb)
            sensor_list.append(cam_seg)

        # ---------------------------------------------------------------------
        # SIMULATION
        #
        world.tick()
        dn.frame_id = 1
        pbar.set_description(config.getTown()[0:6] + " (" + dn.IMAGE_FOLDER[0] + ")")
        pbar.update()
        while dn.frame_id < config.getImNum():
            dn.velocity = vehicle.get_velocity().length()
            if dn.velocity >= dn.MIN_VELOCITY:
                try:
                    for _ in range(len(sensor_list)):
                        semaphore.get(block=True, timeout=5)
                except Empty:
                    pbar.set_description("Sensor error")
                    pbar.close()
                    dn.destroy_carla_object(vehicle_list, sensor_list)
                    sys.exit(2)

            # Update progress bar
                dn.frame_id += 1
                pbar.update()

            # Allow the server to generate the next scene
            [world.tick() for _ in range(round(1/delta_sec))]

        # ---------------------------------------------------------------------
        # CLEANING
        #
        sleep(2)  # allow time to save the last image
        dn.destroy_carla_object(vehicle_list, sensor_list)

        world.apply_settings(dn.carla.WorldSettings(False, False, 0))
        pbar.close()

    except:
        pbar.set_description("Server crash")
        pbar.close()
        dn.destroy_carla_object(vehicle_list, sensor_list)
        sys.exit(3)


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
        '--town',
        default='town01',
        choices=['town01', 'town02', 'town03', 'town04',
                 'town05', 'town06', 'town07', 'town10HD'],
        help='Selected town (default: town01)'
    )
    argparser.add_argument(
        '--speed', '-s',
        default=100,
        type=float,
        help='Vehicles speed percentage (default: 100 => the fastest)'
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
        '--seed',
        type=int,
        default=1,
        help='Seed to initialize random sequences'
    )

    config = Config(argparser.parse_args())
    simulation(config)
    sleep(2)  # allow time to end properly
