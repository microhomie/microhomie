import utime
import settings
from homie import utils

from homie.node.simple import SimpleHomieNode
from homie import HomieDevice

# Homie device setup
homie_device = HomieDevice(settings)

# Adds a simple test node
n = SimpleHomieNode(node_type=b'dummy', node_property=b'value', interval=5)
homie_device.add_node(n)

# Push information about the device to MQTT
homie_device.publish_properties()

while True:
    # try wifi reconnect in case it loses connection
    utils.wifi_connect(settings.WIFI_SSID, settings.WIFI_PASSWORD)

    # Update the data of the simple note for demonstration purpose
    n.value = utime.time()
    print("UPDATED: ".format(n))

    # Push the new data to MQTT
    homie_device.publish_data()

    # Sleep a little bit
    utime.sleep(1)
