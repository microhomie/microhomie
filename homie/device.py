from gc import collect, mem_free
from sys import platform

from asyn import Event
from homie import __version__, utils
from homie.constants import (
    DEVICE_STATE,
    MAIN_DELAY,
    QOS,
    RESTORE_DELAY,
    SLASH,
    STATE_INIT,
    STATE_READY,
    STATE_RECOVER,
    UNDERSCORE,
    UTF8,
    WDT_DELAY,
    T_SET,
    T_BC,
)
from mqtt_as import LINUX, MQTTClient
from uasyncio import get_event_loop, sleep_ms
from ubinascii import hexlify
from utime import time

_EVENT = Event()


# Decorator to block methods and functions until device has "ready" state
def await_ready_state(func):
    def new_gen(*args, **kwargs):
        # fmt: off
        await _EVENT
        await func(*args, **kwargs)
        # fmt: on

    return new_gen


class HomieDevice:

    """MicroPython implementation of the Homie MQTT convention for IoT."""

    def __init__(self, settings):
        self.debug = getattr(settings, "DEBUG", False)
        self._state = STATE_INIT
        self._extensions = getattr(settings, "EXTENSIONS", [])
        self._first_start = True

        self.stats_interval = getattr(settings, "DEVICE_STATS_INTERVAL", 60)

        self.nodes = []
        self.callback_topics = {}

        self.device_name = getattr(settings, "DEVICE_NAME", b"mydevice")

        # Generate unique id if settings has no DEVICE_ID
        try:
            device_id = settings.DEVICE_ID
        except AttributeError:
            device_id = utils.get_unique_id()

        # Base topic
        self.btopic = getattr(settings, "MQTT_BASE_TOPIC", b"homie")
        # Device base topic
        self.dtopic = SLASH.join((self.btopic, device_id))

        self.mqtt = MQTTClient(
            client_id=device_id,
            server=settings.MQTT_BROKER,
            port=getattr(settings, "MQTT_PORT", 1883),
            user=getattr(settings, "MQTT_USERNAME", None),
            password=getattr(settings, "MQTT_PASSWORD", None),
            keepalive=getattr(settings, "MQTT_KEEPALIVE", 30),
            ping_interval=getattr(settings, "MQTT_PING_INTERVAL", 0),
            ssl=getattr(settings, "MQTT_SSL", False),
            ssl_params=getattr(settings, "MQTT_SSL_PARAMS", {}),
            response_time=getattr(settings, "MQTT_RESPONSE_TIME", 10),
            clean_init=getattr(settings, "MQTT_CLEAN_INIT", True),
            clean=getattr(settings, "MQTT_CLEAN", True),
            max_repubs=getattr(settings, "MQTT_MAX_REPUBS", 4),
            will=(SLASH.join((self.dtopic, DEVICE_STATE)), b"lost", True, QOS),
            subs_cb=self.sub_cb,
            wifi_coro=None,
            connect_coro=self.connection_handler,
            ssid=getattr(settings, "WIFI_SSID", None),
            wifi_pw=getattr(settings, "WIFI_PASSWORD", None),
        )

    def add_node(self, node):
        """add a node class of Homie Node to this device"""
        collect()
        node.device = self
        self.nodes.append(node)
        loop = get_event_loop()
        loop.create_task(node.publish_data())

    def format_topic(self, topic):
        if self.dtopic in topic:
            return topic
        return SLASH.join((self.dtopic, topic))

    async def subscribe(self, topic):
        topic = self.format_topic(topic)
        self.dprint("MQTT SUBSCRIBE: {}".format(topic))
        await self.mqtt.subscribe(topic, QOS)

    async def unsubscribe(self, topic):
        topic = self.format_topic(topic)
        self.dprint("MQTT UNSUBSCRIBE: {}".format(topic))
        await self.mqtt.unsubscribe(topic)

    async def add_node_cb(self, node):
        # Add the node callback method only once to the callback list
        nid = node.id.encode()
        if nid not in self.callback_topics:
            self.callback_topics[nid] = node.callback

    async def connection_handler(self, client):
        """subscribe to all registered device and node topics"""
        if self._first_start is False:
            await self.publish(DEVICE_STATE, STATE_RECOVER)

        retained = []
        subscribe = self.subscribe
        unsubscribe = self.unsubscribe

        await self.mqtt.subscribe(
            SLASH.join((self.btopic, b"$broadcast/#")), QOS
        )

        # node topics
        nodes = self.nodes
        for n in nodes:
            props = n._properties
            for p in props:
                if p.restore:
                    # Restore from topic with retained message
                    await self.add_node_cb(n)
                    t = b"{}/{}".format(n.id, p.id)
                    await subscribe(t)
                    retained.append(t)

                if p.settable:
                    await self.add_node_cb(n)
                    await subscribe(b"{}/{}/set".format(n.id, p.id))

        # on first connection:
        # * publish device and node properties
        # * enable WDT
        # * run all coros
        if self._first_start is True:
            await self.publish_properties()

            # unsubscribe from retained topic (restore)
            for t in retained:
                await self.unsubscribe(t)

            self._first_start = False

            # activate WDT
            if LINUX is False and self.debug is False:
                loop = get_event_loop()
                loop.create_task(self.wdt())

            # start coros waiting for ready state
            _EVENT.set()
            await sleep_ms(MAIN_DELAY)
            _EVENT.clear()

        await self.publish(DEVICE_STATE, STATE_READY)

    def sub_cb(self, topic, msg, retained):
        self.dprint("MQTT MESSAGE: {} --> {}, {}".format(topic, msg, retained))

        # Only non-retained messages are allowed on /set topics
        if retained and topic.endswith(T_SET):
            return

        # broadcast callback passed to nodes
        if T_BC in topic:
            nodes = self.nodes
            for n in nodes:
                n.broadcast_callback(topic, msg, retained)
        else:
            # node property callbacks
            nt = topic.split(SLASH)
            node = nt[len(self.dtopic.split(SLASH))]
            if node in self.callback_topics:
                self.callback_topics[node](topic, msg, retained)

    async def publish(self, topic, payload, retain=True):
        if not isinstance(payload, bytes):
            payload = bytes(str(payload), UTF8)

        t = SLASH.join((self.dtopic, topic))
        self.dprint('MQTT PUBLISH: {} --> {}'.format(t, payload))
        await self.mqtt.publish(t, payload, retain, QOS)

    async def broadcast(self, payload, level=None):
        if not isinstance(payload, bytes):
            payload = bytes(str(payload), UTF8)

        topic = SLASH.join((self.btopic, b"$broadcast"))
        if level is not None:
            if isinstance(level, str):
                level = level.encode()
            topic = SLASH.join((topic, level))
        self.dprint("MQTT BROADCAST: {} --> {}".format(topic, payload))
        await self.mqtt.publish(topic, payload, retain=False, qos=QOS)

    async def publish_properties(self):
        """publish device and node properties"""
        publish = self.publish

        # device properties
        await publish(b"$homie", b"4.0.0")
        await publish(b"$name", self.device_name)
        await publish(DEVICE_STATE, STATE_INIT)
        await publish(b"$implementation", bytes(platform, UTF8))
        await publish(
            b"$nodes", b",".join([n.id.encode() for n in self.nodes])
        )

        # node properties
        nodes = self.nodes
        for n in nodes:
            await n.publish_properties()

        if self._extensions:
            await publish(b"$extensions", b",".join(self._extensions))
            if b"org.homie.legacy-firmware:0.1.1:[4.x]" in self._extensions:
                await publish(b"$localip", utils.get_local_ip())
                await publish(b"$mac", utils.get_local_mac())
                await publish(b"$fw/name", b"Microhomie")
                await publish(b"$fw/version", __version__)
            if b"org.homie.legacy-stats:0.1.1:[4.x]" in self._extensions:
                await self.publish(b"$stats/interval", self.stats_interval)
                # Start stats coro
                loop = get_event_loop()
                loop.create_task(self.publish_stats())

    @await_ready_state
    async def publish_stats(self):
        from utime import time

        start_time = time()
        delay = self.stats_interval * MAIN_DELAY
        publish = self.publish
        while True:
            uptime = time() - start_time
            await publish(b"$stats/uptime", uptime)
            await publish(b"$stats/freeheap", mem_free())
            await sleep_ms(delay)

    async def run(self):
        while True:
            try:
                await self.mqtt.connect()
                while True:
                    await sleep_ms(MAIN_DELAY)
            except OSError:
                print("ERROR: can not connect to MQTT")
                await sleep_ms(5000)

    def run_forever(self):
        loop = get_event_loop()
        loop.run_until_complete(self.run())

    async def wdt(self):
        from machine import WDT

        wdt = WDT()
        while True:
            wdt.feed()
            await sleep_ms(WDT_DELAY)

    def dprint(self, *args):
        if self.debug:
            print(*args)

    def start(self):
        # DeprecationWarning
        self.run_forever()
