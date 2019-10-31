import settings
from aswitch import Switch
from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieNodeProperty
from machine import Pin


class ShellyRelay(HomieNode):
    def __init__(self, id, rpin, swpin, name="Light Switch", type="Shelly"):
        super().__init__(id=id, name=name, type=type)
        self.relay = Pin(rpin, Pin.OUT, value=0)
        self.switch = Switch(Pin(swpin, Pin.IN))

        self.relay_property = HomieNodeProperty(
            id="power",
            name=id,
            settable=True,
            retained=True,
            datatype=BOOLEAN,
            default=FALSE,
            restore=True,
        )
        self.add_property(self.relay_property)

        self.switch.open_func(self.toggle, ())
        self.switch.close_func(self.toggle, ())

    def off(self):
        self.relay(0)
        self.relay_property.data = FALSE

    def on(self):
        self.relay(1)
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
    relay1 = ShellyRelay(
        "relay1", rpin=4, swpin=5, name="Light Switch 01", type="Shelly 2.5"
    )
    relay2 = ShellyRelay(
        "relay2", rpin=15, swpin=13, name="Light Switch 02", type="Shelly 2.5"
    )

    homie = HomieDevice(settings)
    homie.add_node(relay1)
    homie.add_node(relay2)
    homie.run_forever()


if __name__ == "__main__":
    main()
