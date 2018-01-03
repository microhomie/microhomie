import utime

from homie.node.simple import SimpleHomieNode

#from homie.node.error import Error


from homie.node.mem import Mem

from homie import HomieDevice

import logging
logger = logging.getLogger('main')

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
node = SimpleHomieNode(b"nodetype", b"node_property")
homie.add_node(node)
#homie.add_node(Error())
homie.add_node(Mem())


# publish device and node properties
homie.publish_properties()
while True:

    # publish device data
    homie.publish_data()

    node.value = utime.time()
    logger.info(str(node.value))

    utime.sleep(1)
