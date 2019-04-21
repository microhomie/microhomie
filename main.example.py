import settings

from machine import Pin

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE


ONOFF = {FALSE: 0, TRUE: 1, 0: FALSE, 1: TRUE}


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

    def callback(self, topic, msg, retained):
        if msg == b"toggle":
            self.led(not self.led())
        else:
            self.led(ONOFF[msg])

        self.led_property.set_data(ONOFF[self.led()])


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED())
    homie.start()


main()
