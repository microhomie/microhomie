from gc import mem_free
from sys import platform
from asyn import Event
from utime import time
from uasyncio import get_event_loop, sleep_ms
from micropython import const

from mqtt_as import MQTTClient
from homie import __version__, utils


QOS = const(1)
MAIN_DELAY = const(5000)
STATS_DELAY = const(60000)
RESTORE_DELAY = const(250)


_EVENT = Event()
def await_ready_state(func):
    def new_gen(*args, **kwargs):
        await _EVENT
        await func(*args, **kwargs)
    return new_gen


class HomieDevice:

    """MicroPython implementation of the Homie MQTT convention for IoT."""

    def __init__(self, settings):
        self._state = "init"
        self._stime = time()

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

        loop = get_event_loop()
        loop.create_task(self.publish_stats())

    def add_node(self, node):
        """add a node class of Homie Node to this device"""
        self.nodes.append(node)
        loop = get_event_loop()
        loop.create_task(node.publish_data(self.publish))

    def format_topic(self, topic):
        return b"/".join((self.dtopic, topic))

    async def subscribe(self, topic, callback=False):
        topic = self.format_topic(topic)
        # print("MQTT SUBSCRIBE: {}".format(topic))
        if callback:
            self.topic_callbacks[topic] = callback
        await self.mqtt.subscribe(topic, QOS)

    async def unsubscribe(self, topic):
        topic = self.format_topic(topic)
        # print("MQTT UNSUBSCRIBE: {}".format(topic))
        await self.mqtt.unsubscribe(topic)
        del self.topic_callbacks[topic]

    async def connection_handler(self, client):
        """subscribe to all registered device and node topics"""
        subscribe = self.subscribe
        unsubscribe = self.unsubscribe

        # device topics
        await self.mqtt.subscribe(
            b"/".join((self.btopic, b"$broadcast/#")), QOS
        )
        await subscribe(b"$stats/interval/set", False)

        # node topics
        nodes = self.nodes
        for n in nodes:
            cb = n.callback
            props = n._properties
            for p in props:
                is_array = p.range > 1
                if p.settable:
                    # subscribe topic to restore retained messages
                    if p.restore:
                        if is_array:
                            t = b"{}/{}_{}".format(self.id, p.id, i)
                        else:
                            t = b"{}/{}".format(n.id, p.id)

                        await subscribe(t, cb)
                        await sleep_ms(RESTORE_DELAY)
                        await unsubscribe(t)

                    # final subscribe to /set topic
                    if is_array:
                        t = b"{}/{}_{}/set".format(self.id, p.id, i)
                    else:
                        t = b"{}/{}/set".format(n.id, p.id)

                    await subscribe(t, cb)

        await self.publish_properties()
        await self.set_state("ready")

    def sub_cb(self, topic, msg, retained):
        # print("MQTT MESSAGE: {} --> {}, {}".format(topic, msg, retained))

        # device callbacks
        if b"/$stats/interval/set" in topic:
            try:
                self.stats_interval = int(msg.decode())
            except ValueError:
                pass
        # broadcast callback passed to nodes
        elif b"/$broadcast" in topic:
            nodes = self.nodes
            for n in nodes:
                n.broadcast_callback(topic, msg, retained)
        else:
            # node property callbacks
            if topic in self.topic_callbacks:
                self.topic_callbacks[topic](topic, msg, retained)

    async def publish(self, topic, payload, retain=True):
        # print('MQTT PUBLISH: {} --> {}'.format(t, payload))
        if not isinstance(payload, bytes):
            payload = bytes(str(payload), "utf-8")
        t = b"/".join((self.dtopic, topic))
        await self.mqtt.publish(t, payload, retain, QOS)

    async def broadcast(self, payload):
        if not isinstance(payload, bytes):
            payload = bytes(str(payload), "utf-8")

        topic = b"/".join((self._rtopic, b"$broadcast"))
        print("MQTT BROADCAST: {} --> {}".format(topic, payload))
        await self.mqtt.publish(topic, payload, retain=False, qos=QOS)

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
        nodes = self.nodes
        for n in nodes:
            try:
                for prop in n.get_properties():
                    await publish(*prop)
            except NotImplementedError:
                raise
            except Exception as error:
                print("ERROR: publish properties for node: {}".format(n))
                print(error)

    @await_ready_state
    async def publish_stats(self):
        stime = self._stime
        interval = self.stats_interval
        publish = self.publish

        while True:
            uptime = time() - stime
            await publish(b"$stats/uptime", uptime)
            await publish(b"$stats/freeheap", mem_free())
            await publish(b"$stats/interval", self.stats_interval)
            await sleep_ms(self.stats_interval * 1000)

            # update interval stats if changed
            if interval != self.stats_interval:
                await publish(b"$stats/interval", self.stats_interval)
                interval = self.stats_interval

    async def set_state(self, val):
        if val in ["ready", "disconnected", "sleeping", "alert"]:
            self._state = val
            await self.publish(b"$state", val)
            if val == "ready":
                _EVENT.set()
                await sleep_ms(1000)
                _EVENT.clear()

    async def run(self):
        try:
            await self.mqtt.connect()
        except OSError:
            print("ERROR: can not connect to MQTT")

        while True:
            await sleep_ms(5000)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
