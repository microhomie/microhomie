import settings

from machine import Pin

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieProperty
from homie.constants import BOOLEAN, FALSE, TRUE


# Reversed values for the esp8266 boards onboard LED
ONOFF = {FALSE: 1, TRUE: 0}


# Initialize the pin for the onboard LED
LED = Pin(2, Pin.OUT, value=1)


# The on_message handler to power the led
def toggle_led(topic, payload, retained):
    LED(ONOFF[payload])


def main():
    # Initialize the Homie device
    device = HomieDevice(settings)

    # Initialize the Homie node for the onboard LED
    led_node = HomieNode(id="led", name="Onboard LED", type="LED",)

    # Initialize the Homie property to power on/off the led
    led_power = HomieProperty(
        id="power",
        name="Power",
        settable=True,
        datatype=BOOLEAN,
        default=FALSE,
        on_message=toggle_led,
    )

    # Add the power property to the node
    led_node.add_property(led_power)

    # Add the led node to the device
    device.add_node(led_node)

    # Run
    device.run_forever()


if __name__ == "__main__":
    main()
