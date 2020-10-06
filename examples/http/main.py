import uasyncio as asyncio

import settings
import urequests

from homie.device import HomieDevice, await_ready_state
from homie.node import HomieNode
from homie.property import HomieProperty


class HTTP(HomieNode):
    def __init__(
        self, url, headers={}, method="GET", name="HTTP request", interval=60
    ):
        super().__init__(id="http", name=name, type="http")
        self.url = url
        self.headers = headers
        self.method = method
        self.interval = interval

        self.p_response = HomieProperty(
            id="response", name="HTTP response"
        )
        self.add_property(self.p_response)

        asyncio.create_task(self.update_data())

    @await_ready_state
    async def update_data(self):
        delay = self.interval * 1000

        while True:
            r = urequests.request(self.method, self.url, headers=self.headers)
            self.p_response.value = r.text
            r.close()

            await asyncio.sleep_ms(delay)


def main():
    homie = HomieDevice(settings)
    homie.add_node(HTTP(url="http://10.0.0.1/status.html"))
    homie.run_forever()


if __name__ == "__main__":
    main()
