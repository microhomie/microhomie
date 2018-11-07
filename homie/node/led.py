from machine import Pin

from homie.node import HomieNode

ONOFF = {b"false": 0, b"true": 1, 0: b"false", 1: b"true"}


class LED(HomieNode):
    def __init__(self, name="Device LED", pin=2):
        super().__init__(name=name)
        self.node_id = b"led"
        self.pin = pin
        self.led = Pin(pin, Pin.OUT, value=0)
        self.updated = True

    def __str__(self):
        return "LED status = {}".format(ONOFF[self.led()])

    @property
    def subscribe(self):
        yield b"led/power/set"

    def get_properties(self):
        yield (b"led/$name", self.name)
        yield (b"led/$type", b"led")
        yield (b"led/$properties", b"power")
        yield (b"led/power/$name", b"LED")
        yield (b"led/power/$settable", b"true")
        yield (b"led/power/$datatype", b"string")
        yield (b"led/power/$format", b"true,false,toggle")

    def callback(self, topic, msg):
        if msg == b"toggle":
            self.led(not self.led())
        else:
            self.led(ONOFF[msg])

        self.updated = True

    def has_update(self):
        if self.updated is True:
            self.updated = False
            return True
        return False

    def get_data(self):
        yield (b"led/power", ONOFF[self.led()])
