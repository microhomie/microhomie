from gc import mem_free
from sys import platform
from utime import time
from micropython import const

import uasyncio as asyncio

from mqtt_as import MQTTClient
from homie import __version__, utils


QOS = const(1)


class HomieDevice:

    """MicroPython implementation of the Homie MQTT convention for IoT."""

    def __init__(self, settings):
        self._state = "init"

        self.errors = 0
        self.start_time = time()
        self.stats_interval = settings.DEVICE_STATS_INTERVAL

        self.nodes = []
        self.topic_callbacks = {}

        self.device_name = settings.DEVICE_NAME

        self.btopic = settings.MQTT_BASE_TOPIC
        self.dtopic = b"/".join((settings.MQTT_BASE_TOPIC, settings.DEVICE_ID))

        # setup networking
        utils.setup_network()
        utils.wifi_connect()

        self.mqtt = MQTTClient(
            client_id=settings.DEVICE_ID,
            server=settings.MQTT_BROKER,
            port=settings.MQTT_PORT,
            user=settings.MQTT_USERNAME,
            password=settings.MQTT_PASSWORD,
            keepalive=settings.MQTT_KEEPALIVE,
            ssl=settings.MQTT_SSL,
            ssl_params=settings.MQTT_SSL_PARAMS,
            subs_cb=self.sub_cb,
            connect_coro=self.connection_handler,
            will=(b"/".join((self.dtopic, b"$state")), b"lost", True, QOS),
        )

    def add_node(self, node):
        """add a node class of Homie Node to this device"""
        self.nodes.append(node)

    async def connection_handler(self, client):
        """subscribe to all registered device and node topics"""
        base = self.dtopic
        subscribe = self.mqtt.subscribe

        # device topics
        await subscribe(b"/".join((base, b"$stats/interval/set")), QOS)
        await subscribe(b"/".join((self.btopic, b"$broadcast/#")), QOS)

        # subscribe to node topics
        nodes = self.nodes
        for n in nodes:
            for t in n.subscribe():
                t = b"/".join((base, t))
                # print('MQTT SUBSCRIBE: {}'.format(t))
                await subscribe(t, QOS)
                self.topic_callbacks[t] = n.callback

        await self.publish_properties()
        await self.set_state("ready")

        loop = asyncio.get_event_loop()
        loop.create_task(self.publish_stats())

        for n in self.nodes:
            loop.create_task(n.publish_data(self))

    def sub_cb(self, topic, msg, retained):
        # print('MQTT MESSAGE: {} --> {}, {}'.format(topic, msg, retained))

        # device callbacks
        if b"/$stats/interval/set" in topic:
            try:
                self.stats_interval = int(msg.decode())
            except ValueError:
                pass
        # broadcast callback passed to nodes
        elif b"/$broadcast" in topic:
            for n in self.nodes:
                n.broadcast_callback(topic, msg, retained)
        else:
            # node property callbacks
            if topic in self.topic_callbacks:
                self.topic_callbacks[topic](topic, msg, retained)

    async def publish(self, topic, payload, retain=True):
        if not isinstance(payload, bytes):
            payload = bytes(str(payload), "utf-8")
        t = b"/".join((self.dtopic, topic))
        # print('MQTT PUBLISH: {} --> {}'.format(t, payload))
        await self.mqtt.publish(t, payload, retain=retain, qos=QOS)

    async def publish_properties(self):
        """publish device and node properties"""
        publish = self.publish

        # device properties
        await publish(b"$homie", b"3.0.1")
        await publish(b"$name", self.device_name)
        await publish(b"$state", b"init")
        await publish(b"$fw/name", b"Microhomie")
        await publish(b"$fw/version", __version__)
        await publish(b"$implementation", bytes(platform, "utf-8"))
        await publish(b"$localip", utils.get_local_ip())
        await publish(b"$mac", utils.get_local_mac())
        await publish(b"$stats", b"interval,uptime,freeheap")
        await publish(b"$stats/interval", self.stats_interval)
        await publish(
            b"$nodes", b",".join([n.id.encode() for n in self.nodes])
        )

        # node properties
        for n in self.nodes:
            try:
                for prop in n.get_properties():
                    await publish(*prop)
            except NotImplementedError:
                raise
            except Exception as error:
                print("ERROR: publish properties for node: {}".format(n))
                print(error)

    async def publish_stats(self):
        interval = self.stats_interval
        while True:
            uptime = time() - self.start_time
            await self.publish(b"$stats/uptime", uptime)
            await self.publish(b"$stats/freeheap", mem_free())
            await asyncio.sleep(self.stats_interval)

            # update interval stats if changed
            if interval != self.stats_interval:
                await self.publish(b"$stats/interval", self.stats_interval)
                interval = self.stats_interval

    async def set_state(self, val):
        if val in ["ready", "disconnected", "sleeping", "alert"]:
            self._state = val
            await self.publish(b"$state", val)

    async def run(self):
        try:
            await self.mqtt.connect()
        except OSError:
            print("ERROR: can not connect to MQTT")
            return

        while True:
            await asyncio.sleep(5)
