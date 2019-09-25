import uos
import settings

from time import sleep_ms
from machine import Pin
from aswitch import Pushbutton

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE


def reset(led):
    import machine
    wdt = machine.WDT()
    wdt.feed()
    while True:
        led(not led())
        sleep_ms(250)


class SmartSocket(HomieNode):
    def __init__(self):
        super().__init__(id="relay", name="Relay 16A", type="Gosund SP1 v23")
        uos.dupterm(None, 1)  # disable REPL so we can use the blue led
        self.led_b = Pin(1, Pin.OUT, value=1)
        self.led_r = Pin(13, Pin.OUT, value=1)
        self.relay = Pin(14, Pin.OUT)

        self.relay_property = HomieNodeProperty(
            id="power",
            name="Relay",
            settable=True,
            retained=True,
            datatype="bool",
            default=FALSE,
            restore=True,
        )
        self.add_property(self.relay_property)

        self.button = Pushbutton(Pin(3, Pin.IN))
        self.button.release_func(self.toggle, ())
        self.button.long_func(reset, (self.led_r,))

    def off(self):
        self.relay(0)
        self.led_b(0)
        self.led_r(1)
        self.relay_property.data = FALSE

    def on(self):
        self.relay(1)
        self.led_b(1)
        self.led_r(0)
        self.relay_property.data = TRUE

    def callback(self, topic, payload, retained):
        if b"power" in topic:
            if payload == FALSE:
                self.off()
            elif payload == TRUE:
                self.on()

    def toggle(self):
        if self.relay_property.data == TRUE:
            self.off()
        else:
            self.on()


def main():
    homie = HomieDevice(settings)
    homie.add_node(SmartSocket())
    homie.run_forever()


if __name__ == "__main__":
    sleep_ms(500)
    main()
