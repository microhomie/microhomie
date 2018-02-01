"""
Install micropython via https://github.com/micropython/micropython


micropython -m upip install micropython-collections

"""


import utime
import settings
from homie.node.simple import SimpleHomieNode
from homie.node.error import Error
from homie import HomieDevice


print('PLEASE RUN THIS ONLY IN A MICROPYTHON ENVIRONMENT')
print('SEE DOCUMENTATION FOR DETAILS:')
print('...')
utime.sleep(2)


homie_device = HomieDevice(settings)

n = SimpleHomieNode(node_type=b'dummy', node_property=b'value', interval=5)
n.value = 17

homie_device.add_node(n)
homie_device.add_node(Error())
homie_device.publish_properties()

while True:
    homie_device.publish_data()
    n.value = utime.time()
    print('INFO: {}'.format(n))
    utime.sleep(1)
