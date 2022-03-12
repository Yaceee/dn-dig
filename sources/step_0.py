import daynightdl as dn
import config as conf

from time import sleep


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

        # weather and vehicle
        dn.set_weather(world, is_sun=True)
        vehicle = dn.set_autonom_car(world, tag="model3", tm_port=0)

        # ---------------------------------------------------------------------
        # MAIN LOOP
        #
        sleep(60)

    # -------------------------------------------------------------------------
    # CLEANING
    #
    finally:
        world.apply_settings(original_settings)
        vehicle.destroy()
        print("Cleaned up")
