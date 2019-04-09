import settings

from machine import Pin

from homie.node import HomieNodeProperty, HomieNode
from homie.device import HomieDevice


ONOFF = {b"false": 0, b"true": 1, 0: b"false", 1: b"true"}


class LED(HomieNode):
    def __init__(self, name="Device LED", pin=2):
        super().__init__(id="led", name=name, type="LED")
        self.pin = pin
        self.led = Pin(pin, Pin.OUT, value=0)
        self.updated = True

        self.led_property = HomieNodeProperty(
            id="power",
            name="LED",
            settable=True,
            datatype="enum",
            format="true,false,toggle",
            restore=True,
            default=b"true",
        )

        self.add_property(self.led_property)

    def __str__(self):
        return "LED status: {}".format(ONOFF[self.led()])

    def callback(self, topic, msg, retained):
        if msg == b"toggle":
            self.led(not self.led())
        else:
            self.led(ONOFF[msg])

        self.led_property.set_data(0, ONOFF[self.led()])
        self.updated = True

    def has_update(self):
        if self.updated is True:
            self.updated = False
            return True
        return False


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED())
    homie.start()


main()
