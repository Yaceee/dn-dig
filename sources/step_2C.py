import daynightdl as dn
import config as conf

from queue import Queue
from queue import Empty
from time import sleep

def simulation(is_sun):
    try:
        client = dn.carla.Client(conf.host, conf.port) # connect to the server
        client.set_timeout(10.0)
        world = client.get_world()

        # Load the desired map
        client.load_world("Town10HD_Opt")

        # Set synchronous mode settings
        original_settings = world.get_settings()
        new_settings = world.get_settings()
        new_settings.synchronous_mode = True
        new_settings.fixed_delta_seconds = 1/conf.FRAME_PER_S
        world.apply_settings(new_settings)

        client.reload_world(False) # reload map keeping the world settings

        # Set up the traffic manager
        traffic_manager = client.get_trafficmanager(conf.tm_port)
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(conf.SEED) # define TM seed for determinism

        # Spawn your vehicles, pedestrians, etc.
        # weather and vehicle
        # value_if if condition else value_else
        dn.IMAGE_FOLDER = "DAY" if is_sun else "NIGHT"
        dn.set_weather(world, is_sun=is_sun)
        vehicle = dn.set_autonom_car(world, tag="model3", tm_port=conf.tm_port)
        traffic_manager.ignore_lights_percentage(vehicle, 100)
        
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

        # Simulation loop
        dn.frame_id = 1
        while dn.frame_id < conf.IM_NUMBER:
            try:
                for _ in range(len(sensor_list)):
                    s_frame = sensor_queue.get(block=True, timeout=0.25)
                    print("Frame: %d Sensor: %s" % (s_frame[0], s_frame[1]))
                dn.frame_id += 1
            except Empty:
                print("Some of the sensor information is missed")
            for _ in range(conf.FRAME_PER_S):
                world.tick()
    finally:
        world.apply_settings(original_settings)
        vehicle.destroy()
        for sensor in sensor_list:
            sensor.stop()
            sensor.destroy()
        print("Cleaned up")


if __name__ == "__main__":
    simulation(is_sun = True)
    simulation(is_sun = False)
    sleep(1) # allow last image to be saved by the camera thread
