import dht
import settings
import uasyncio as asyncio

from homie.device import HomieDevice, await_ready_state
from homie.node import HomieNode
from homie.property import HomieProperty
from homie.constants import FLOAT
from machine import Pin


class DHT22(HomieNode):
    def __init__(self, name="Temp & Humid", pin=4, interval=60, pull=-1):
        super().__init__(id="dht22", name=name, type="dht22")
        self.dht22 = dht.DHT22(Pin(pin, Pin.IN, pull))
        self.interval = interval

        self.p_temp = HomieProperty(
            id="temperature",
            name="Temperature",
            datatype=FLOAT,
            format="-40:80",
            unit="°C",
        )
        self.add_property(self.p_temp)

        self.p_humid = HomieProperty(
            id="humidity",
            name="Humidity",
            datatype=FLOAT,
            format="0:100",
            unit="%",
        )
        self.add_property(self.p_humid)

        asyncio.create_task(self.update_data())

    @await_ready_state
    async def update_data(self):
        dht22 = self.dht22
        delay = self.interval * 1000

        while True:
            dht22.measure()
            self.p_temp.data = dht22.temperature()
            self.p_humid.data = dht22.humidity()

            await asyncio.sleep_ms(delay)


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add dht22 node
    homie.add_node(DHT22(pin=4))

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
