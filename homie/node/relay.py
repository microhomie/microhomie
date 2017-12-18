"""
import utime

from homie.node.relay import Relay
from homie import HomieDevice

CONFIG = {
    'mqtt': {
        'broker': 'localhost',
    }
}

homie = HomieDevice(CONFIG)
homie.add_node(Relay(pin=[2, 4]))

homie.publish_properties()

while True:
    homie.publish_data()
    homie.mqtt.check_msg()
    utime.sleep(0.5)
"""

from machine import Pin

from . import HomieNode


ONOFF = {b'off': 0, b'on': 1, 0: b'off', 1: b'on'}


class Relay(HomieNode):

    def __init__(self, pin, interval=1):
        super().__init__(interval=interval)
        self.has_new_update = True
        self.subscribe = []
        self.relais = []
        self.onoff = ONOFF
        for p in pin:
            p = Pin(p, Pin.OUT, value=0)
            self.relais.append(p)

        self.sub()

    def __str__(self):
        pass

    def get_properties(self):
        relais = len(self.relais)
        properties_str = 'relay[1-{}]'.format(relais).encode()
        properties = [
            (b'relay/$type', b'relay'),
            (b'relay/$properties', properties_str),
        ]

        for relay in range(relais):
            name = 'Relay {}'.format(relay + 1).encode()
            prop = 'relay/relay_{}'.format(relay + 1).encode()
            attributes = [
                (prop + b'/$settable', b'true'),
                (prop + b'/$name', name),
                (prop + b'/$datatype', b'string'),
                (prop + b'/$format', b'on,off')
            ]
            properties.extend(attributes)

        return properties

    def sub(self):
        for relay in range(len(self.relais)):
            relay += 1
            self.subscribe.append('relay/relay_{}/set'.format(relay).encode())

    def callback(self, topic, message):
        topic = topic.decode()
        relay = int('/'.join(topic.split('/')[2:-1]).split('_')[1]) - 1
        self.relais[relay].value(self.onoff[message])
        self.has_new_update = True

    def has_update(self):
        if self.has_new_update is True:
            self.has_new_update = False
            return True
        return False

    def get_data(self):
        data = []
        for relay in range(len(self.relais)):
            topic = 'relay/relay_{}'.format(relay + 1).encode()
            data.append((topic, self.onoff[self.relais[relay].value()]))

        return data
