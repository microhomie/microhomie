import asyn
import settings
from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty
from machine import Pin
from micropython import const
from uasyncio import get_event_loop, sleep_ms


PIR_DELAY = const(20)


class PIR(HomieNode):
    def __init__(self, name="Motion sensor", pin=4):
        super().__init__(id="pir", name=name, type="PIR")
        self.pir = Pin(pin, Pin.IN, pull=Pin.PULL_UP)
        self.active = True

        self.pir_property = HomieNodeProperty(
            id="active",
            name="PIR Status",
            settable=True,
            datatype=BOOLEAN,
            restore=True,
            default=TRUE,
        )

    def callback(self, topic, payload, retained):
        if b"active" in topic:
            if payload == FALSE:
                if self.active:
                    asyn.launch(asyn.NamedTask.cancel, ("pir_sensor",))
                    self.active = False
            elif payload == TRUE:
                if not self.active:
                    self.active = True
                    loop = get_event_loop()
                    loop.create_task(
                        asyn.NamedTask("pir_sensor", self.pir_sensor)()
                    )
            else:
                return

            self.pir_property.data = payload
            if retained:
                self.pir_sensor.update_delta()

    async def pir_sensor(self):
        pir = self.pir
        latest = 0

        while True:
            s = pir()
            if s != latest and s == 1:
                latest = s
                self.device.broadcast("motion detected")

            await sleep_ms(PIR_DELAY)


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add PIR node to device
    homie.add_node(PIR())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
