import utime
import settings

from homie.node.error import Error
from homie import HomieDevice
from machine import WDT


wdt = WDT(timeout=3000)

homie = HomieDevice(settings)

homie.add_node(Error())

# publish device and node properties
homie.publish_properties()

while True:
    # reset the errors
    homie.errors = 0

    # publish device data
    homie.publish_data()

    # feed wdt if we have no errors
    if not homie.errors:
        wdt.feed()

    utime.sleep(1)
