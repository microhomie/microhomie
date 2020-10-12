import pycom
import uasyncio
import settings

from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty
from homie.constants import FALSE, TRUE, BOOLEAN


class Heartbeat(HomieNode):
    def __init__(self, name="Heartbeat LED", pin=2):
        super().__init__(id="heartbeat", name=name, type="WS2812 LED")

        self.power_property = HomieNodeProperty(
            id="power",
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=TRUE,
        )
        self.add_property(self.power_property, self.on_power_msg)

        # Heartbeat default on
        pycom.heartbeat(True)

    def on_power_msg(self, topic, payload, retained):
        if payload == TRUE:
            pycom.heartbeat(True)
        else:
            pycom.heartbeat(False)

        self.power_property.data = payload


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    homie.add_node(Heartbeat())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
