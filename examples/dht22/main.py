import dht
import settings

from machine import Pin
from uasyncio import get_event_loop, sleep_ms

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty


class DHT22(HomieNode):

    def __init__(self, name="Temp & Hum", pin=4, interval=60, pull=-1):
        super().__init__(id="dht22", name=name, type="dht22")
        self.dht22 = dht.DHT22(Pin(pin, Pin.IN, pull))
        self.interval = interval

        self.temp_property = HomieNodeProperty(
            id="temperature",
            name="Temperature",
            datatype="float",
            format="-40:80",
            unit="°C",
        )
        self.add_property(self.temp_property)

        self.hum_property = HomieNodeProperty(
            id="humidity",
            name="Humidity",
            datatype="float",
            format="0:100",
            unit="%",
        )
        self.add_property(self.hum_property)

        loop = get_event_loop()
        loop.create_task(self.update_data())

    async def update_data(self):
        dht22 = self.dht22
        delay = self.interval * 1000

        while True:
            dht22.measure()
            self.temp_property.set_data(dht22.temperature())
            self.hum_property.set_data(dht22.humidity())

            await sleep_ms(delay)


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add dht22 node
    homie.add_node(DHT22(pin=4))

    # run forever
    homie.start()


if __name__ == "__main__":
    main()
