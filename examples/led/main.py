import settings

from machine import Pin

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE


ONOFF = {FALSE: 1, TRUE: 0, 1: FALSE, 0: TRUE}


class LED(HomieNode):
    def __init__(self, name="Device LED", pin=2):
        super().__init__(id="led", name=name, type="LED")
        self.pin = pin
        self.led = Pin(pin, Pin.OUT, value=0)

        self.led_property = HomieNodeProperty(
            id="power",
            name="LED",
            settable=True,
            datatype="enum",
            format="true,false,toggle",
            restore=True,
            default=TRUE,
        )

        self.add_property(self.led_property)

    def callback(self, topic, payload, retained):
        if b"led/power" in topic:
            if payload == b"toggle":
                self.led(not self.led())
            else:
                self.led(ONOFF[payload])

            self.led_property.data = ONOFF[self.led()]


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED())

    # run forever
    homie.start()


if __name__ == "__main__":
    main()
