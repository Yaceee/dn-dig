import daynightdl as dn
import config as conf
from tqdm import tqdm

from queue import Queue, Empty
from time import sleep


def simulation(is_sun):
    try:
        # ---------------------------------------------------------------------
        # INITIALIZATION
        #
        # client
        client = dn.carla.Client(conf.HOST, conf.PORT)
        client.set_timeout(10.0)


        # set world mode to synchronous
        world = client.get_world()
        world.apply_settings(
                dn.carla.WorldSettings(synchronous_mode=True,
                                       no_rendering_mode=False,
                                       fixed_delta_seconds=0.05))

        # Set up the traffic manager
        traffic_manager = client.get_trafficmanager(conf.TM_PORT)
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(conf.TM_SEED)

        # weather
        dn.IMAGE_FOLDER = "DAY" if is_sun else "NIGHT"
        dn.set_weather(world, is_sun=is_sun)

        # car configuration
        vehicle = dn.set_autonom_car(world, tag="model3", tm_port=conf.TM_PORT)
        traffic_manager.ignore_lights_percentage(vehicle, 100)

        # attach cameras to the vehicle
        sensor_list = []
        sensor_queue = Queue()

        cam_semantic = dn.camera_init(
            "sensor.camera.semantic_segmentation",
            conf.SEG_TAG,
            world,
            vehicle,
            sensor_queue,
        )
        cam_rgb = dn.camera_init(
            "sensor.camera.rgb", conf.RGB_TAG, world, vehicle, sensor_queue
        )

        sensor_list.append(cam_semantic)
        sensor_list.append(cam_rgb)

        # ---------------------------------------------------------------------
        # SIMULATION
        #
        world.tick()
        print(f"Recording {dn.IMAGE_FOLDER} images")
        for dn.frame_id in tqdm(range(1, conf.IM_NUMBER+1)):
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
        world.apply_settings(dn.carla.WorldSettings(False, False, 0))
        vehicle.destroy()
        for sensor in sensor_list:
            sensor.stop()
            sensor.destroy()
        print("Server cleaned")


if __name__ == '__main__':
    simulation(is_sun = True)
    simulation(is_sun = False)
    sleep(1) # allow time for saving the last image
