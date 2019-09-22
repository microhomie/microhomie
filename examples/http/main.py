import settings
import urequests
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty
from uasyncio import get_event_loop, sleep_ms


class HTTP(HomieNode):
    def __init__(
        self, url, headers={}, method="GET", name="HTTP request", interval=60
    ):
        super().__init__(id="http", name=name, type="http")
        self.url = url
        self.headers = headers
        self.method = method
        self.interval = interval

        self.response_property = HomieNodeProperty(
            id="response", name="HTTP response"
        )
        self.add_property(self.response_property)

        loop = get_event_loop()
        loop.create_task(self.update_data())

    async def update_data(self):
        delay = self.interval * 1000

        while True:
            r = urequests.request(self.method, self.url, headers=self.headers)
            self.response_property.data = r.text
            r.close()

            await sleep_ms(delay)


def main():
    homie = HomieDevice(settings)
    homie.add_node(HTTP(url="http://10.0.0.1/status.html"))
    homie.start()


if __name__ == "__main__":
    main()
