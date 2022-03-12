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
        client = dn.carla.Client(host=conf.host, port=conf.port)
        client.set_timeout(2.0)

        # world settings
        world = client.get_world()
        original_settings = world.get_settings()
        settings = world.get_settings()

        # set the syncronous mode
        settings.fixed_delta_seconds = 0.2
        settings.synchronous_mode = True
        world.apply_settings(settings)

        # weather and vehicle
        dn.set_weather(world, is_sun=True)
        vehicle = dn.set_autonom_car(world, tag="model3", tm_port=0)

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

        # ---------------------------------------------------------------------
        # MAIN LOOP
        #
        for _ in range(conf.IM_NUMBER):
            world.tick()
            try:
                for _ in range(len(sensor_list)):
                    s_frame = sensor_queue.get(block=True, timeout=1.0)
                    print("Frame: %d Sensor: %s" % (s_frame[0], s_frame[1]))

            except Empty:
                print("Some of the sensor information is missed")
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
