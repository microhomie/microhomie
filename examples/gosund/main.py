import uos
import settings

from time import sleep_ms
from machine import Pin
from primitives.pushbutton import Pushbutton

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE, BOOLEAN


def reset(led):
    import machine
    wdt = machine.WDT()
    wdt.feed()
    while True:
        led(not led())
        sleep_ms(250)


class SmartSocket(HomieNode):
    def __init__(self, name="Relay 16A"):
        super().__init__(id="relay", name=name, type="Gosund SP1")

        # disable REPL so we can use the blue led
        uos.dupterm(None, 1)

        self.led_b = Pin(1, Pin.OUT, value=1)  # Blue LED
        self.led_r = Pin(13, Pin.OUT, value=1)  # Red LED
        self.relay = Pin(14, Pin.OUT)

        self.power_property = HomieNodeProperty(
            id="power",
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
        )
        self.add_property(self.power_property, self.on_power_msg)

        self.button = Pushbutton(Pin(3, Pin.IN))
        self.button.release_func(self.toggle, ())
        self.button.long_func(reset, (self.led_r,))

    def off(self):
        self.relay(0)
        self.led_b(0)
        self.led_r(1)
        self.power_property.data = FALSE

    def on(self):
        self.relay(1)
        self.led_b(1)
        self.led_r(0)
        self.power_property.data = TRUE

    def on_power_msg(self, topic, payload, retained):
        if payload == FALSE:
            self.off()
        elif payload == TRUE:
            self.on()

    def toggle(self):
        if self.power_property.data == TRUE:
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
