"""
Install micropython via https://github.com/micropython/micropython


micropython -m upip install -p app micropython-umqtt.simple micropython-collections
MICROPYPATH=app micropython test.py
"""

import sys
import utime
import settings
from homie.node import HomieNode
from homie.node.simple import SimpleHomieNode
from homie import HomieDevice

try:
    if sys.implementation.name != 'micropython':
        raise NotImplementedError
except Exception:
    print('PLEASE RUN THIS ONLY IN A MICROPYTHON ENVIRONMENT')
    print('SEE DOCUMENTATION FOR DETAILS:')
    print('...')
    sys.exit()


# Error Node for tests
class Error(HomieNode):

    def has_update(self):
        return True

    def __str__(self):
        return "ErrorNode"

    def get_properties(self):
        raise Exception('ErrorNode Test Exception - get_properties')

    def get_data(self):
        raise Exception('ErrorNode Test Exception - get_data')

    def update_data(self):
        raise Exception('ErrorNode Test Exception - update_data')

    def callback(self, topic, payload):
        raise Exception('ErrorNode Test Exception - callback')

    def broadcast_callback(self, payload):
        raise Exception('ErrorNode Test Exception - broadcast_callback')

    def get_node_id(self):
        raise Exception('ErrorNode Test Exception - get_node_id')


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
