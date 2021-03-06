import daynightdl as dn
import config as conf
from tqdm import tqdm

from queue import Queue, Empty
from time import sleep


def simulation(client, is_sun, confObj):
    try:
        # ---------------------------------------------------------------------
        # INITIALIZATION
        #
        # load the specified world
        try:
            world = client.load_world(confObj.town)
        except RuntimeError:
            print(f"{confObj.town} not found, use the current world")
            world = client.get_world()

        # set world mode to synchronous
        world.apply_settings(
                dn.carla.WorldSettings(synchronous_mode=True,
                                       no_rendering_mode=False,
                                       fixed_delta_seconds=0.05))

        # Set up the traffic manager
        TM_PORT = 8000
        traffic_manager = client.get_trafficmanager(TM_PORT)
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(1)

        # weather
        dn.IMAGE_FOLDER = "DAY" if is_sun else "NIGHT"
        dn.set_weather(world, is_sun, confObj)

        # set traffic and pick the first car
        vehicle_list = dn.set_autonom_car(world, confObj, TM_PORT)
        vehicle = vehicle_list[0]
        traffic_manager.ignore_lights_percentage(vehicle, 100)

        # attach cameras to the vehicle
        sensor_list = []
        sensor_queue = Queue()

        cam_seg = dn.camera_init("seg", world, vehicle, sensor_queue, confObj)
        cam_rgb = dn.camera_init("rgb", world, vehicle, sensor_queue, confObj)

        sensor_list.append(cam_seg)
        sensor_list.append(cam_rgb)

        # ---------------------------------------------------------------------
        # SIMULATION
        #
        world.tick()
        print(f"Recording {dn.IMAGE_FOLDER} images")
        for dn.frame_id in tqdm(range(1, confObj.imNum+1)):
            try:
                for _ in range(len(sensor_list)):
                    s_frame = sensor_queue.get(block=True, timeout=1)
            except Empty:
                continue
            for _ in range(20):
                world.tick()
        #
        # ---------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # CLEANING
    #
    finally:
        for vehicle in vehicle_list:
            vehicle.destroy()
        for sensor in sensor_list:
            sensor.stop()
            sensor.destroy()

        world.apply_settings(dn.carla.WorldSettings(False, False, 0))
        print("Server cleaned")


if __name__ == '__main__':
    # client
    client = dn.carla.Client(conf.globalConf.host, conf.globalConf.port)
    client.set_timeout(10.0)

    # simulations
    simulation(client, is_sun = True,  confObj=conf.globalConf)
    simulation(client, is_sun = False, confObj=conf.globalConf)
    sleep(1) # allow time for saving the last image
