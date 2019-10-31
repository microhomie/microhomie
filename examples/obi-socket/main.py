from time import sleep_ms

import settings
from aswitch import Pushbutton
from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty
from machine import Pin


def reset(led):
    import machine

    wdt = machine.WDT()
    wdt.feed()
    led(0)
    machine.reset()


class SmartSocket(HomieNode):
    def __init__(self):
        super().__init__(
            id="relay", name="Wifi Power Socket", type="OW8266-02Q"
        )
        self.led = Pin(4, Pin.OUT, value=1)
        self.r_on = Pin(12, Pin.OUT)
        self.r_off = Pin(5, Pin.OUT)

        self.relay_property = HomieNodeProperty(
            id="power",
            name="Relay",
            settable=True,
            retained=True,
            datatype=BOOLEAN,
            default=FALSE,
            restore=True,
        )
        self.add_property(self.relay_property)

        self.button = Pushbutton(Pin(14, Pin.IN, Pin.PULL_UP))
        self.button.release_func(self.toggle, ())
        self.button.long_func(reset, (self.led,))

    def off(self):
        self.r_off(0)
        sleep_ms(100)
        self.r_on(1)
        self.relay_property.data = FALSE

    def on(self):
        self.r_on(0)
        sleep_ms(100)
        self.r_off(1)
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
    main()
