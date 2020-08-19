import uasyncio as asyncio

from gc import collect, mem_free
from sys import platform

from homie import __version__
from homie.network import get_local_ip, get_local_mac
from homie.constants import (
    DEVICE_STATE,
    MAIN_DELAY,
    QOS,
    SLASH,
    STATE_OTA,
    STATE_INIT,
    STATE_READY,
    STATE_RECOVER,
    STATE_WEBREPL,
    T_BC,
    T_MPY,
    T_SET,
    UNDERSCORE,
    UTF8,
    WDT_DELAY,
    EXT_MPY,
    EXT_FW,
    EXT_STATS,
)
from machine import RTC, reset
from mqtt_as import LINUX, MQTTClient
from uasyncio import sleep_ms
from ubinascii import hexlify
from utime import time
from primitives import launch
from primitives.message import Message


def get_unique_id():
    if LINUX is False:
        from machine import unique_id
        return hexlify(unique_id()).decode()
    else:
        raise NotImplementedError(
            "Linux doesn't have a unique id. Provide the DEVICE_ID option in your settings.py."
        )


# Decorator to block async tasks until the device is in "ready" state
_MESSAGE = Message()
def await_ready_state(func):
    def new_gen(*args, **kwargs):
        # fmt: off
        await _MESSAGE
        await func(*args, **kwargs)
        # fmt: on

    return new_gen


class HomieDevice:

    """MicroPython implementation of the Homie MQTT convention for IoT."""

    def __init__(self, settings):
        self.debug = getattr(settings, "DEBUG", False)

        self._state = STATE_INIT
        self._version = __version__
        self._fw_name = "Microhomie"
        self._extensions = getattr(settings, "EXTENSIONS", [])
        self._bc_enabled = getattr(settings, "BROADCAST", False)

        self.first_start = True
        self.stats_interval = getattr(settings, "DEVICE_STATS_INTERVAL", 60)
        self.device_name = getattr(settings, "DEVICE_NAME", "")
        self.callback_topics = {}

        # Registered homie nodes
        self.nodes = []

        # Generate unique id if settings has no DEVICE_ID
        self.device_id = getattr(settings, "DEVICE_ID", get_unique_id())

        # Base topic
        self.btopic = getattr(settings, "MQTT_BASE_TOPIC", "homie")
        # Device base topic
        self.dtopic = "{}/{}".format(self.btopic, self.device_id)

        self.mqtt = MQTTClient(
            client_id=self.device_id,
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
            will=("{}/{}".format(self.dtopic, DEVICE_STATE), "lost", True, QOS),
            subs_cb=self.subs_cb,
            wifi_coro=None,
            connect_coro=self.connection_handler,
            ssid=getattr(settings, "WIFI_SSID", None),
            wifi_pw=getattr(settings, "WIFI_PASSWORD", None),
        )

    def add_node(self, node):
        node.device = self
        node.set_topic()  # set topic for node properties
        _p = node.properties
        for p in _p:
            p.set_topic()
        self.nodes.append(node)

    def all_properties(self, func, tup_args):
        """ Run method on all registered property objects """
        _n = self.nodes
        for n in _n:
            _p = n.properties
            for p in _p:
                func = getattr(p, func)
                launch(func, tup_args)

    async def subscribe(self, topic):
        self.dprint("MQTT SUBSCRIBE: {}".format(topic))
        await self.mqtt.subscribe(topic, QOS)

    async def unsubscribe(self, topic):
        self.dprint("MQTT UNSUBSCRIBE: {}".format(topic))
        await self.mqtt.unsubscribe(topic)

    async def connection_handler(self, client):
        """subscribe to all registered device and node topics"""
        if not self.first_start:
            await self.publish("{}/{}".format(self.dtopic, DEVICE_STATE), STATE_RECOVER)

        # Subscribe to Homie broadcast topic
        if self._bc_enabled:
            await self.subscribe("{}/{}/#".format(self.btopic, T_BC))

        # Subscribe to the Micropython extension topic
        if EXT_MPY in self._extensions:
            await self.subscribe("{}/{}".format(self.dtopic, T_MPY))

        # Subscribe to node property topics
        self.all_properties("subscribe", ())

        # on first connection:
        # * publish device and node properties
        # * enable WDT
        # * run all coros
        if self.first_start is True:
            await self.publish_properties()

            # Unsubscribe from retained topics that received no retained message
            for t in self.callback_topics:
                if not t.endswith(T_SET):
                    await self.unsubscribe(t)
                    del self.callback_topics[t]

            # Activate watchdog timer
            if not LINUX and not self.debug:
                asyncio.create_task(self.wdt())

            # Start all async tasks decorated with await_ready_state
            _MESSAGE.set()
            await sleep_ms(MAIN_DELAY)
            _MESSAGE.clear()

            # Do not run this if clause again on wifi/broker reconnect
            self.first_start = False

            # Publish data from all properties on first start
            self.all_properties("publish", ())

        # Announce that the device is ready
        await self.publish("{}/{}".format(self.dtopic, DEVICE_STATE), STATE_READY)

    def subs_cb(self, topic, payload, retained):
        """ The main callback for all subscribed topics """
        topic = topic.decode()
        payload = payload.decode()

        self.dprint(
            "MQTT MESSAGE: {} --> {}, {}".format(topic, payload, retained)
        )

        # Only non-retained messages are allowed on /set topics
        if retained and topic.endswith(T_SET):
            return

        # broadcast topic
        if T_BC in topic:
            self.broadcast_callback(topic, payload, retained)
        # Micropython extension
        elif topic.endswith(T_MPY) and EXT_MPY in self._extensions:
            if payload == "reset":
                asyncio.create_task(self.reset("reset"))
            elif payload == "webrepl":
                asyncio.create_task(self.reset("webrepl"))
            elif payload == "yaota8266" and platform == "esp8266":
                asyncio.create_task(self.reset("yaotaota"))
        # All other topics
        else:
            if topic in self.callback_topics:
                self.callback_topics[topic](topic, payload, retained)

    async def publish(self, topic, payload, retain=True):
        if isinstance(payload, int):
            payload = str(payload).encode()

        if isinstance(payload, str):
            payload = payload.encode()

        self.dprint("MQTT PUBLISH: {} --> {}".format(topic, payload))
        await self.mqtt.publish(topic, payload, retain, QOS)

    async def broadcast(self, payload, level=None):
        if isinstance(payload, int):
            payload = str(payload)

        topic = "{}/{}".format(self.btopic, T_BC)
        if level is not None:
            topic = "{}/{}".format(topic, level)
        self.dprint("MQTT BROADCAST: {} --> {}".format(topic, payload))
        await self.mqtt.publish(topic, payload, retain=False, qos=QOS)

    def broadcast_callback(self, topic, payload, retained):
        """ Gets called when the broadcast topic receives a message """
        pass

    async def publish_properties(self):
        """ Publish device and node properties """
        _t = self.dtopic
        publish = self.publish

        # device properties
        await publish("{}/$homie".format(_t), "4.0.0")
        await publish("{}/$name".format(_t), self.device_name)
        await publish("{}/{}".format(_t, DEVICE_STATE), STATE_INIT)
        await publish("{}/$implementation".format(_t), bytes(platform, UTF8))
        await publish(
            "{}/$nodes".format(_t), ",".join([n.id for n in self.nodes])
        )

        # node properties
        _n = self.nodes
        for n in _n:
            await n.publish_properties()

        # extensions
        await publish("{}/$extensions".format(_t), ",".join(self._extensions))
        if EXT_FW in self._extensions:
            await publish("{}/$localip".format(_t), get_local_ip())
            await publish("{}/$mac".format(_t), get_local_mac())
            await publish("{}/$fw/name".format(_t), self._fw_name)
            await publish("{}/$fw/version".format(_t), self._version)
        if EXT_STATS in self._extensions:
            await self.publish("{}/$stats/interval".format(_t), str(self.stats_interval))
            # Start stats coro
            asyncio.create_task(self.publish_stats())

    @await_ready_state
    async def publish_stats(self):
        from utime import time

        _d = self.stats_interval * 1000  # delay
        _st = time()  # start time
        _tup = "{}/$stats/uptime".format(self.dtopic)  # Uptime topic
        _tfh = "{}/$stats/freeheap".format(self.dtopic)  # Freeheap topic

        publish = self.publish
        while True:
            uptime = time() - _st
            await publish(_tup, str(uptime))
            await publish(_tfh, str(mem_free()))
            await sleep_ms(_d)

    async def run(self):
        while True:
            try:
                await self.mqtt.connect()
                while True:
                    collect()
                    await sleep_ms(MAIN_DELAY)
            except OSError:
                print("ERROR: can not connect to MQTT")
                await sleep_ms(5000)
            except Exception:
                print("Exception! Fix this line!")

    def run_forever(self):
        if RTC().memory() == b"webrepl":
            RTC().memory(b"")
        else:
            asyncio.run(self.run())

    async def reset(self, reason):
        if reason != "reset":
            RTC().memory(reason)
        await self.publish("{}/{}".format(self.dtopic, DEVICE_STATE), reason)
        await self.mqtt.disconnect()
        await sleep_ms(500)
        reset()

    async def wdt(self):
        from machine import WDT

        wdt = WDT()
        while True:
            wdt.feed()
            await sleep_ms(WDT_DELAY)

    def dprint(self, *args):
        if self.debug:
            print(*args)
