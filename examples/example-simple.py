import utime

from homie.node.simple import SimpleHomieNode
from homie import HomieDevice

CONFIG = {
    'mqtt': {
        'broker': 'localhost',
        'base_topic': b'uhomie'
    },
    'device': {
        'id': b'esp8266',
    }
}

homie = HomieDevice(CONFIG)

node = SimpleHomieNode("nodetype", "node_property")

homie.add_node(node)

# publish device and node properties
homie.publish_properties()

while True:

    # publish device data
    homie.publish_data()
    
    node.value = utime.time()

    utime.sleep(1)
