import asyn
import settings
from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty
from machine import Pin
from micropython import const
from uasyncio import get_event_loop, sleep_ms


_SENSOR = "sensor"
_PIR_DELAY = const(20)


class PIR(HomieNode):
    def __init__(self, name="Motion sensor", pin=4):
        super().__init__(id="pir", name=name, type="PIR")
        self.pir = Pin(pin, Pin.IN, pull=Pin.PULL_UP)
        self.active = True

        self.active_property = HomieNodeProperty(
            id="active",
            name="PIR Status",
            settable=True,
            datatype=BOOLEAN,
            restore=True,
            default=TRUE,
        )
        self.add_property(self.active_property, self.on_active_msg)

    def on_active_msg(self, topic, payload, retained):
        if payload == FALSE:
            if self.active:
                asyn.launch(asyn.NamedTask.cancel, (_SENSOR,))
                self.active = False
        elif payload == TRUE:
            if not self.active:
                self.active = True
                loop = get_event_loop()
                loop.create_task(
                    asyn.NamedTask(_SENSOR, self.pir_sensor)()
                )
        else:
            return

        self.active_property.data = payload

    async def pir_sensor(self):
        pir = self.pir
        latest = 0

        while True:
            s = pir()
            if s != latest and s == 1:
                latest = s
                self.device.broadcast("motion detected")

            await sleep_ms(_PIR_DELAY)


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add PIR node to device
    homie.add_node(PIR())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
