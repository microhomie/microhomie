"""
Example device and node for the ESP8266 onboard LED.

The onboard led status is reversed to the pin status. On start the onboard
LED is on. To turn it off send 'on' or 'toggle' via mqtt:

$ mosquitto_pub -t 'homie/esp8266/led/power/set' -m on
$ mosquitto_pub -t 'homie/esp8266/led/power/set' -m off
$ mosquitto_pub -t 'homie/esp8266/led/power/set' -m toggle
"""

import settings

from homie.node.led import LED
from homie.device import HomieDevice


def main():
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED(pin=2))

    # run forever
    homie.start()


main()
