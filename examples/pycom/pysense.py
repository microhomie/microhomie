from SI7006A20 import SI7006A20

from homie.node import HomieNode
from homie.property import HomieNodeProperty
from homie.constants import FLOAT
from uasyncio import get_event_loop, sleep_ms


class SI7006A20Node(HomieNode):
    def __init__(self, interval=60):
        super().__init__(
            id="si7006a20",
            name="Humidity and Temperature Sensor",
            type="SI7006A20",
        )
        self.interval = interval
        self.sensor = SI7006A20()

        self.temp_property = HomieNodeProperty(
            id="temperature",
            name="Temperature",
            datatype=FLOAT,
            format="-40:80",
            unit="°C",
        )
        self.add_property(self.temp_property)

        self.hum_property = HomieNodeProperty(
            id="humidity",
            name="Humidity",
            datatype=FLOAT,
            format="0:100",
            unit="%",
        )
        self.add_property(self.hum_property)

        loop = get_event_loop()
        loop.create_task(self.update_data())

    async def update_data(self):
        s = self.sensor
        d = self.interval * 1000

        while True:
            self.temp_property.data = s.temperature()
            self.hum_property.data = s.humidity()
            await sleep_ms(d)
