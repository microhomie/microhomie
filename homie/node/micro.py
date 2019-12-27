from machine import RTC, reset
from uasyncio import sleep_ms

from homie.constants import FALSE, TRUE, BOOLEAN, ENUM
from homie.node import HomieNode
from homie.property import HomieNodeProperty


class MPy(HomieNode):
    def __init__(self, webrepl_pass="uhomie"):
        super().__init__(id="mpy", name="Micropython", type="system")
        self.webrepl_pass = webrepl_pass  # webrepl password

        self.webrepl_property = HomieNodeProperty(
            id="webrepl",
            name="WebREPL",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
        )
        self.add_property(self.webrepl_property, self.on_webrepl_msg)

        self.cmd_property = HomieNodeProperty(
            id="cmd",
            name="Command",
            settable=True,
            datatype=ENUM,
            format="reset,yaota8266",
            retained=False,
        )
        self.add_property(self.cmd_property, self.on_cmd_msg)

    def on_webrepl_msg(self, topic, payload, retained):
        import webrepl

        if payload == FALSE:
            webrepl.stop()
        elif payload == TRUE:
            webrepl.start(password=self.webrepl_pass)

        self.webrepl_property.data = payload

    def on_cmd_msg(self, topic, payload, retained):
        if payload == "reset":
            reset()
        elif payload == "yaota8266":
            from asyn import launch
            launch(self.yaotaota_init, ())

    async def yaotaota_init(self):
        RTC().memory(b"yaotaota")
        await self.device.mqtt.disconnect()
        await sleep_ms(1000)
        reset()
