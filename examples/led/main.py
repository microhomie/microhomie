import settings

from machine import Pin
from primitives.pushbutton import Pushbutton

from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieProperty


class LED(HomieNode):

    # Reversed values for the esp8266 boards onboard led
    ONOFF = {FALSE: 1, TRUE: 0}

    def __init__(self, name="Onboard LED", pin=0):
        super().__init__(id="led", name=name, type="LED")
        self.led = Pin(pin, Pin.OUT, value=1)

        # Boot button on some dev boards
        self.btn = Pushbutton(Pin(pin, Pin.IN, Pin.PULL_UP))
        self.btn.press_func(self.toggle_led)

        self.p_power = HomieProperty(
            id="power",
            name="LED Power",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
            on_message=self.on_power_msg,
        )
        self.add_property(self.p_power)

    def on_power_msg(self, topic, payload, retained):
        self.led(self.ONOFF[payload])

    def toggle_led(self):
        if self.p_power.value == TRUE:
            self.led(1)
        else:
            self.led(0)


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
