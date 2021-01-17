import settings

from homie.constants import TRUE, BOOLEAN
from homie.node import ArrayNode
from homie.device import HomieDevice
from homie.property import ArrayProperty, get_index_from_set_topic


class LEDArrayNode(ArrayNode):
    def __init__(self, array=16):
        super().__init__(id="led", name="LED", type="LED", array=array)

        # No LEDs setup in this example to power on/off.

        self.p_power = ArrayProperty(
            id="power",
            array=array,
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=TRUE,
            on_message=self.on_power_msg,
        )
        self.add_property(self.p_power)

    def on_power_msg(self, topic, payload, retained):
        index = get_index_from_set_topic(topic)
        if index is None:  # loop over all array properties
            for index, value in enumerate(self.p_power):
                self.p_power[index] = payload


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LEDArrayNode())

    # run forever
    homie.run_forever()


if __name__ == "__main__":
    main()
