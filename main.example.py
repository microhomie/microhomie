import utime
from homie.node.simple import SimpleHomieNode
from homie.node.mem import Mem

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

simple_node = SimpleHomieNode(b"nodetype", b"node_property")
homie.add_node(simple_node)
homie.add_node(Mem())


# publish device and node properties
homie.publish_properties()
while True:

    # publish device data
    homie.publish_data()

    simple_node.value = utime.time()
    print(simple_node.value)

    utime.sleep(1)
