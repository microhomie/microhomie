import settings

from homie.device import HomieDevice

from heartbeat import Heartbeat
from pysense import SI7006A20Node


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    homie.add_node(Heartbeat())
    homie.add_node(SI7006A20Node())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
