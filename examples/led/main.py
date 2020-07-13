import settings

from machine import Pin
from primitives.pushbutton import Pushbutton

from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty


# Reversed values for the esp8266 boards onboard led
ONOFF = {FALSE: 1, TRUE: 0, 1: FALSE, 0: TRUE}


class LED(HomieNode):
    def __init__(self, name="Onboard LED", pin=2):
        super().__init__(id="led", name=name, type="LED")
        self.pin = pin
        self.led = Pin(pin, Pin.OUT, value=0)

        # Boot button on some dev boards
        self.btn = Pushbutton(Pin(0, Pin.IN, Pin.PULL_UP))
        self.btn.press_func(self.toggle_led)

        self.p_power = HomieNodeProperty(
            id="power",
            name="LED Power",
            settable=True,
            datatype=BOOLEAN,
            default=TRUE,
            on_message=self.on_power_msg,
        )
        self.add_property(self.p_power)

    def on_power_msg(self, topic, payload, retained):
        self.led(ONOFF[payload])
        self.p_power.data = payload

    def toggle_led(self):
        print(self.p_power.value)
        if self.p_power.value == TRUE:
            self.led(1)
            self.p_power.value = FALSE
        else:
            self.led(0)
            self.p_power.value = TRUE


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
