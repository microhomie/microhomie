import utime
import settings

from homie.node.simple import SimpleHomieNode
from homie import HomieDevice, utils

# Network Setup
utils.disable_ap()  # on esp devices
utils.wifi_connect()

# Homie device setup
homie_device = HomieDevice(settings)

# Adds a simple test node
n = SimpleHomieNode(node_type=b'dummy', node_property=b'value', interval=5)
homie_device.add_node(n)

# Push information about the device to MQTT
homie_device.publish_properties()

while True:
    # try wifi reconnect in case it loses connection
    if not utils.wlan.isconnected():
        utils.wifi_connect()

    # Update the data of the simple note for demonstration purpose
    n.value = utime.time()
    print("UPDATED: ".format(n))

    # Push the new data to MQTT
    homie_device.publish_data()

    # Sleep a little bit
    utime.sleep(1)
