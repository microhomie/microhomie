import gc
import sys

from homie import __version__, utils
from umqtt.simple import MQTTClient
from utime import sleep, time


class HomieDevice:

    """MicroPython implementation of the Homie MQTT convention for IoT."""

    def __init__(self, settings):
        self._state = "init"
        self.mqtt = None
        self.errors = 0
        self.settings = settings

        self.retry_delay = 10

        self.nodes = []
        self.node_ids = []
        self.topic_callbacks = {}

        self.start_time = time()
        self.next_update = time()
        self.stats_interval = self.settings.DEVICE_STATS_INTERVAL

        # device base topic
        self.topic = b"/".join(
            (self.settings.MQTT_BASE_TOPIC, self.settings.DEVICE_ID)
        )

        # setup wifi
        utils.setup_network()
        utils.wifi_connect()

        try:
            self._umqtt_connect()
        except Exception:
            print("ERROR: can not connect to MQTT")
            # self.mqtt.publish = lambda topic, payload, retain, qos: None

    def _umqtt_connect(self):
        mqtt = MQTTClient(
            self.settings.DEVICE_ID,
            self.settings.MQTT_BROKER,
            port=self.settings.MQTT_PORT,
            user=self.settings.MQTT_USERNAME,
            password=self.settings.MQTT_PASSWORD,
            keepalive=self.settings.MQTT_KEEPALIVE,
            ssl=self.settings.MQTT_SSL,
            ssl_params=self.settings.MQTT_SSL_PARAMS,
        )

        mqtt.DEBUG = True

        mqtt.set_callback(self.sub_cb)  # for all callbacks
        mqtt.set_last_will(
            b"/".join((self.topic, b"$state")), b"lost", retain=True, qos=1
        )

        mqtt.connect()
        self.mqtt = mqtt

    def add_node(self, node):
        """add a node class of HomieNode to this device"""
        self.nodes.append(node)

        # add node_ids
        try:
            if node.node_id != b"$stats":
                self.node_ids.append(node.node_id)
        except NotImplementedError:
            raise
        except Exception:
            print("ERROR: getting Node")

    def subscribe_topics(self):
        """subscribe to all registered device and node topics"""
        base = self.topic
        subscribe = self.mqtt.subscribe

        # device topics
        subscribe(b"/".join((base, b"$stats/interval/set")))
        subscribe(b"/".join((base, b"$broadcast/#")))

        # node topics
        nodes = self.nodes
        for node in nodes:
            for topic in node.subscribe:
                # print('MQTT SUBSCRIBE: {}'.format(b'/'.join((base, topic))))
                subscribe(b"/".join((base, topic)))
                self.topic_callbacks[topic] = node.callback

    def sub_cb(self, topic, message):
        # device callbacks
        # print('MQTT MESSAGE: {} --> {}'.format(topic, message))

        if b"/$stats/interval/set" in topic:
            self.stats_interval = int(message.decode())
            self.publish(b"$stats/interval", self.stats_interval)
            self.next_update = time() + self.stats_interval
        elif b"/$broadcast" in topic:
            for node in self.nodes:
                node.broadcast(topic, message)
        else:
            # node property callbacks
            if topic in self.topic_callbacks:
                self.topic_callbacks[topic](topic, message)

    def publish(self, topic, payload, retain=True):
        # try wifi reconnect in case it lost connection
        utils.wifi_connect()

        if not isinstance(payload, bytes):
            payload = bytes(str(payload), "utf-8")
        t = b"/".join((self.topic, topic))
        done = False
        while not done:
            try:
                # print('MQTT PUBLISH: {} --> {}'.format(t, payload))
                self.mqtt.publish(t, payload, retain=retain, qos=1)
                done = True
            except Exception:
                # some error during publishing
                done = False
                done_reconnect = False
                sleep(self.retry_delay)
                # tries to reconnect
                while not done_reconnect:
                    try:
                        self._umqtt_connect()
                        self.publish_properties()  # re-publish
                        self.subscribe_topics()  # re-subscribe
                        done_reconnect = True
                    except Exception as e:
                        done_reconnect = False
                        print("ERROR: cannot connect, {}".format(str(e)))
                        sleep(self.retry_delay)

    def publish_properties(self):
        """publish device and node properties"""
        publish = self.publish

        # device properties
        publish(b"$homie", b"3.0.1")
        publish(b"$name", self.settings.DEVICE_NAME)
        publish(b"$state", b"init")
        publish(b"$fw/name", self.settings.DEVICE_FW_NAME)
        publish(b"$fw/version", __version__)
        publish(b"$implementation", bytes(sys.platform, "utf-8"))
        publish(b"$localip", utils.get_local_ip())
        publish(b"$mac", utils.get_local_mac())
        publish(b"$stats", b"interval,uptime,freeheap")
        publish(b"$stats/interval", self.stats_interval)
        publish(b"$nodes", b",".join(self.node_ids))

        # node properties
        for node in self.nodes:
            try:
                for propertie in node.get_properties():
                    publish(*propertie)
            except NotImplementedError:
                raise
            except Exception as error:
                self.node_error(node, error)

    def publish_data(self):
        """publish node data if node has updates"""
        self.publish_device_stats()
        publish = self.publish

        # node data
        for node in self.nodes:
            try:
                if node.has_update():
                    for data in node.get_data():
                        publish(*data)
            except NotImplementedError:
                raise
            except Exception as error:
                self.node_error(node, error)

    def publish_device_stats(self):
        _time = time
        if _time() > self.next_update:
            uptime = _time() - self.start_time
            self.publish(b"$stats/uptime", uptime)
            self.publish(b"$stats/freeheap", gc.mem_free())
            # set next update
            self.next_update = _time() + self.stats_interval

    def set_state(self, state):
        if state in ["ready", "disconnected", "sleeping", "alert"]:
            self._state = state
            self.publish(b"$state", state)

    def node_error(self, node, error):
        self.errors += 1
        print("ERROR: during publish_data for node: {}".format(node))
        print(error)

    def start(self):
        """publish device and node properties, run forever"""
        self.publish_properties()
        self.subscribe_topics()
        gc.collect()

        self.set_state("ready")

        while True:
            try:
                if not utils.wlan.isconnected():
                    utils.wifi_connect()

                # publish device data
                self.publish_data()

                # check for new mqtt messages
                self.mqtt.check_msg()

                sleep(1)
            except KeyboardInterrupt:
                self.set_state("disconnected")
                self.mqtt.disconnect()
