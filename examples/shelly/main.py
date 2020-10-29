import settings

from machine import Pin
from primitives.switch import Switch
from micropython import const

from homie.constants import FALSE, TRUE, BOOLEAN
from homie.device import HomieDevice
from homie.node import HomieNode
from homie.property import HomieProperty


_ON = const(1)
_OFF = const(0)


class ShellyRelay(HomieNode):
    def __init__(self, id="relay", rpin=4, swpin=5, name="Light Switch", type="Shelly"):
        super().__init__(id=id, name=name, type=type)
        self.relay = Pin(rpin, Pin.OUT, value=0)
        self.switch = Switch(Pin(swpin, Pin.IN))

        self.p_power = HomieProperty(
            id="power",
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
            on_message=self.on_power_msg,
        )
        self.add_property(self.p_power)

        self.switch.open_func(self.toggle, ())
        self.switch.close_func(self.toggle, ())

    def on_power_msg(self, topic, payload, retained):
        if payload == FALSE:
            self.relay(_OFF)
        elif payload == TRUE:
            self.relay(_ON)

    def toggle(self):
        if self.power_property.value == TRUE:
            self.relay(_OFF)
            self.p_power.value = FALSE
        elif self.power_property.value == FALSE:
            self.relay(_ON)
            self.p_power.value = TRUE


def main():
    # Make a homie device
    homie = HomieDevice(settings)

    # Shelly 1 example
    relay = ShellyRelay()
    homie.add_node(relay)

    # Shelly 2.5 example
    # relay_1 = ShellyRelay("relay_1", rpin=4, swpin=5, name="Indoor", type="Shelly 2.5")
    # homie.add_node(relay_1)

    # relay_2 = ShellyRelay("relay_2", rpin=4, swpin=5, name="Outdoor", type="Shelly 2.5")
    # homie.add_node(relay_2)

    # Startup device
    homie.run_forever()


if __name__ == "__main__":
    main()
