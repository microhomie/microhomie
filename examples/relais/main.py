import settings

from machine import Pin

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE


POWER = {
    TRUE: 0,
    FALSE: 1,
}


class Relais(HomieNode):
    def __init__(self):
        super().__init__(id="relay", name="Relay Board", type="relayboard")
        self.relais = [
            Pin(2, Pin.OUT),
            Pin(4, Pin.OUT),
        ]

        self.relay_property = HomieNodeProperty(
            id="power",
            name="Relay",
            settable=True,
            retained=True,
            datatype="bool",
            default=TRUE,
            restore=True,
            range=2,
        )
        self.add_property(self.relay_property)

    def callback(self, topic, msg, retained):
        if b"power" in topic:
            if msg in [TRUE, FALSE]:
                relay = self.get_property_id_from_set_topic(topic)
                if relay is not None:
                    self.relay_property[relay] = msg
                    self.relais[relay](POWER[msg])


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add PIR node to device
    homie.add_node(Relais())

    # run forever
    homie.start()


if __name__ == "__main__":
    main()
