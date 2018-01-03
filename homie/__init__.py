import sys
import utime
#import logging
import ubinascii
import machine
#logger = logging.getLogger('device')
#logger.level = logging.ERROR
from umqtt.robust import MQTTClient

__version__ = b'0.1.0'

def get_local_ip():
    try:
        import network
        return bytes(network.WLAN(0).ifconfig()[0], 'utf-8')
    except:
        return "127.0.0.1"

def get_local_mac():
    try:
        import network
        return ubinascii.hexlify(network.WLAN(0).config('mac'), ':')
    except:
        return "cannotgetlocalmac"



# Default config
CONFIG = {
    'mqtt': {
        'broker': '127.0.0.1',
        'port': 0,
        'user': None,
        'pass': None,
        'keepalive': 60,
        'ssl': False,
        'ssl_params': {},
        'base_topic': b'homie'
    },
    'device': {
        'id': ubinascii.hexlify(machine.unique_id()),
        'name': b'mydevice',
        'fwname': b'uhomie',
        'fwversion': __version__,
        'localip': get_local_ip(),
        'mac': get_local_mac(),
        'platform': bytes(sys.platform, 'utf-8'),
        'stats_interval': 60
    }
}


class HomieDevice:

    """ MicroPython implementation of the homie v2 convention. """

    def __init__(self, cfg=None):
        #internal error counter
        self.errors = 0

        self.nodes = []
        self.topic_callbacks = {}

        # update config
        if cfg is not None:
            if 'mqtt' in cfg:
                CONFIG['mqtt'].update(cfg['mqtt'])
            if 'device' in cfg:
                CONFIG['device'].update(cfg['device'])

        self.start_time = utime.time()
        self.next_update = utime.time()
        self.stats_interval = CONFIG['device']['stats_interval']

        # base topic
        self.topic = b'/'.join((CONFIG['mqtt']['base_topic'],
                               CONFIG['device']['id']))

        # mqtt client
        self.mqtt = MQTTClient(
            CONFIG['device']['id'],
            CONFIG['mqtt']['broker'],
            port=CONFIG['mqtt']['port'],
            user=CONFIG['mqtt']['user'],
            password=CONFIG['mqtt']['pass'],
            keepalive=CONFIG['mqtt']['keepalive'],
            ssl=CONFIG['mqtt']['ssl'],
            ssl_params=CONFIG['mqtt']['ssl_params'])

        self.mqtt.DEBUG = True

        # set callback
        self.mqtt.set_callback(self.sub_cb)

        # set last will testament
        self.mqtt.set_last_will(self.topic + b'/$online', b'false',
                                retain=True, qos=1)

        try:
            self.mqtt.connect()

            # subscribe to device topics
            self.mqtt.subscribe(self.topic + b'/$stats/interval/set')
            self.mqtt.subscribe(self.topic + b'/$broadcast/#')
        except:
            logger.error("Error connecting to MQTT")
            #self.mqtt.publish = lambda topic, payload, retain, qos: None


    def add_node(self, node):
        """add a node class of HomieNode to this device"""
        self.nodes.append(node)
        # subscribe node topics
        for topic in node.subscribe:
            topic = b'/'.join((self.topic, topic))
            self.mqtt.subscribe(topic)
            self.topic_callbacks[topic] = node.callback

    def sub_cb(self, topic, message):
        # device callbacks
        if b'$stats/interval/set' in topic:
            self.stats_interval = int(message.decode())
            self.publish(b'$stats/interval', self.stats_interval, True)
            self.next_update = utime.time() + self.stats_interval
        elif b'$broadcast/#' in topic:
            for node in self.nodes:
                node.broadcast(topic, message)
        else:
            # process node callbacks
            if topic in self.topic_callbacks:
                self.topic_callbacks[topic](topic, message)

    def publish(self, topic, payload, retain=True, qos=1):
        try:
            print("start publish")
            if not isinstance(payload, bytes):
                payload = bytes(str(payload), 'utf-8')
            t = b'/'.join((self.topic, topic))
            print(str(t))
            ret = self.mqtt.publish(t, payload, retain=retain, qos=qos)
            print(ret)
            print("publish done")
        except Exception as e:
            #logger.error("Problem publishing ")
            #logger.error(str(e))
            print(str(e))
            self.errors += 1

    def publish_properties(self):
        """publish device and node properties"""
        # node properties
        properties = (
            (b'$homie', b'2.1.0', True),
            (b'$online', b'true', True),
            (b'$fw/name', CONFIG['device']['fwname'], True),
            (b'$fw/version', CONFIG['device']['fwversion'], True),
            (b'$implementation', CONFIG['device']['platform'], True),
            (b'$localip', CONFIG['device']['localip'], True),
            (b'$mac', CONFIG['device']['mac'], True),
            (b'$stats/interval', self.stats_interval, True),
        )


        # publish all properties
        for prop in properties:
            self.publish(*prop)

        # device properties
        for node in self.nodes:
            try:
                for prop in node.get_properties():
                    self.publish(*prop)
            except Exception as e:
                print("error")

    def publish_data(self):
        """publish node data if node has updates"""
        self.publish_device_stats()
        # node data
        for node in self.nodes:
            try:
                if node.has_update():
                    for prop in node.get_data():
                        #logger.debug(str(prop))
                        self.publish(*prop)
            except Exception as e:
                #logger.error(str(e))
                self.errors += 1

    def publish_device_stats(self):
        if utime.time() > self.next_update:
            # uptime
            uptime = utime.time() - self.start_time
            self.publish(b'$stats/uptime', uptime, True)
            # set next update
            self.next_update = utime.time() + self.stats_interval
