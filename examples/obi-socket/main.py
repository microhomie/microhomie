import settings
import uasyncio as asyncio

from primitives.pushbutton import Pushbutton
from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieProperty
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

        self.p_power = HomieProperty(
            id="power",
            name="Relay",
            settable=True,
            retained=True,
            datatype=BOOLEAN,
            default=FALSE,
            restore=True,
            on_message=self.on_power_msg,
        )
        self.add_property(self.p_power)

        self.button = Pushbutton(Pin(14, Pin.IN, Pin.PULL_UP))
        self.button.release_func(self.toggle, ())
        self.button.long_func(reset, (self.led,))

    async def off(self):
        self.r_off(0)
        await asyncio.sleep_ms(100)
        self.r_on(1)

    async def on(self):
        self.r_on(0)
        await asyncio.sleep_ms(100)
        self.r_off(1)

    def on_power_msg(self, topic, payload, retained):
        if payload == FALSE:
            self.off()
        elif payload == TRUE:
            self.on()

    async def toggle(self):
        if self.p_power.value == TRUE:
            await self.off()
            self.p_power.value = FALSE
        else:
            await self.on()
            self.p_power.value = TRUE


def main():
    homie = HomieDevice(settings)
    homie.add_node(SmartSocket())
    homie.run_forever()


if __name__ == "__main__":
    main()
