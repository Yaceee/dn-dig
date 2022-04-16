import daynightdl as dn
import argparse
from config import Config

from tqdm import tqdm
from queue import Queue, Empty
from time import sleep


def simulation(config : Config):
    try:
        # ---------------------------------------------------------------------
        # INITIALIZATION
        #
        # client
        print(config)
        client = dn.carla.Client(config.getHost(), config.getPort())
        client.set_timeout(10.0)

        # load the specified world
        try:
            world = client.load_world(config.town)
        except RuntimeError:
            print(f"{config.town} not found, use the current world")
            world = client.get_world()

        # set world mode to synchronous
        delta_sec = 0.1
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
        traffic_manager.set_random_device_seed(1)

        # weather
        dn.IMAGE_FOLDER = "DAY" if config.angle >= 0 else "NIGHT"
        dn.set_weather(world, config)

        # set traffic and pick the first car
        vehicle_list = dn.set_autonom_car(world, config,traffic_manager , TM_PORT)
        vehicle = vehicle_list[0]
        traffic_manager.ignore_lights_percentage(vehicle, 100)

        # attach cameras to the vehicle
        sensor_list = []
        sensor_queue = Queue()

        cam_seg = dn.camera_init("seg", world, vehicle, sensor_queue, config)
        cam_rgb = dn.camera_init("rgb", world, vehicle, sensor_queue, config)

        sensor_list.append(cam_seg)
        sensor_list.append(cam_rgb)

        # ---------------------------------------------------------------------
        # SIMULATION
        #
        world.tick()
        print(f"Recording {dn.IMAGE_FOLDER} images")
        for dn.frame_id in tqdm(range(1, config.imNum+1)):
            try:
                for _ in range(len(sensor_list)):
                    sensor_queue.get(block=True, timeout=5)
            except Empty:
                print("Sensor error")
                continue
            for _ in range(int(config.fps/delta_sec)):
                world.tick()
        #
        # ---------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # CLEANING
    #
    finally:
        sleep(2)  # allow time to save the last image

        for sensor in sensor_list:
            sensor.stop()
            sensor.destroy()
        for vehicle in vehicle_list:
            vehicle.destroy()

        world.apply_settings(dn.carla.WorldSettings(False, False, 0))
        print("Server cleaned")


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
        '--town', '-t',
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

    config = argparser.parse_args()
    conf_obj = Config(config.host, config.port, config.tag, config.town, config.fov, config.dimension[0], config.dimension[1], config.imNum, config.angle, config.traffic, config.speed)

    simulation(conf_obj)

    sleep(2)  # allow time to save the last image
