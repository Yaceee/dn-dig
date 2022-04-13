import daynightdl as dn
import config as conf

from queue import Queue
from queue import Empty


if __name__ == "__main__":
    try:
        # ---------------------------------------------------------------------
        # INITIALIZATION
        #
        # client
        client = dn.carla.Client(host=conf.HOST, port=conf.PORT)
        client.set_timeout(2.0)

        # world settings
        world = client.get_world()
        original_settings = world.get_settings()

        # set the syncronous mode
        new_settings = world.get_settings()
        new_settings.synchronous_mode = True
        new_settings.fixed_delta_seconds = 0.05
        world.apply_settings(new_settings)

        #client.reload_world(False) # reload map keeping the world settings

        # Set up the traffic manager
        traffic_manager = client.get_trafficmanager(conf.TM_PORT)
        traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_random_device_seed(conf.TM_SEED)

        # weather and vehicle
        dn.set_weather(world, is_sun=True)
        dn.IMAGE_FOLDER = "DAY"
        vehicle = dn.set_autonom_car(world, tag="model3", tm_port=conf.TM_PORT)
        traffic_manager.ignore_lights_percentage(vehicle, 100)

        # sensors
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

        client.start_recorder("recorder/recording01.log")

        # ---------------------------------------------------------------------
        # MAIN LOOP
        #
        dn.frame_id = 1
        while dn.frame_id < conf.IM_NUMBER:
            try:
                for _ in range(len(sensor_list)):
                    s_frame = sensor_queue.get(block=True, timeout=1.0)
                    print("Frame: %d Sensor: %s" % (s_frame[0], s_frame[1]))
                dn.frame_id += 1

            except Empty:
                print("Some of the sensor information is missed")

            for _ in range(20):
                world.tick()
        #
        # ---------------------------------------------------------------------

        client.stop_recorder()

        # ---------------------------------------------------------------------
        # REPLAY
        #
        # switch to night
        dn.set_weather(world, is_sun=False)
        dn.IMAGE_FOLDER = "NIGHT"

        # replay
        client.replay_file(
            "recorder/recording01.log", start=0, duration=0, follow_id=vehicle
        )
        #
        # ---------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # CLEANING
    #
    finally:
        world.apply_settings(original_settings)
        vehicle.destroy()
        for sensor in sensor_list:
            sensor.stop()
            sensor.destroy()
        print("Cleaned up")
