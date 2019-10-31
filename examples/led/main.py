import settings
from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty
from machine import Pin


# reversed values for the esp8266 boards onboard led
ONOFF = {FALSE: 1, TRUE: 0, 1: FALSE, 0: TRUE}


class LED(HomieNode):
    def __init__(self, name="Onboard LED", pin=2):
        super().__init__(id="led", name=name, type="LED")
        self.pin = pin
        self.led = Pin(pin, Pin.OUT, value=0)

        self.led_property = HomieNodeProperty(
            id="power",
            name="LED Power",
            settable=True,
            datatype=BOOLEAN,
            restore=True,
            default=TRUE,
        )

        self.add_property(self.led_property)

    def callback(self, topic, payload, retained):
        if b"led/power" in topic:
            if payload == self.led_property.data:
                return

            self.led(ONOFF[payload])
            self.led_property.data = ONOFF[self.led()]


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
