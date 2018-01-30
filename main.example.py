import utime
import settings

from homie.node.simple import SimpleHomieNode
from homie import HomieDevice


homie_device = HomieDevice(settings)

n = SimpleHomieNode(node_type=b'dummy', node_property=b'value', interval=5)
n.value = 17

homie_device.add_node(n)
homie_device.publish_properties()

while True:
    homie_device.publish_data()
    n.value = utime.time()
    print(n)
    utime.sleep(1)
