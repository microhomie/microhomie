import neopixel
import settings

from machine import Pin

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def all_off(np):
    np.fill(BLACK)
    np.write()


def all_on(np, color=WHITE):
    np.fill(color)
    np.write()


def convert_str_to_rgb(rgb_str):
    try:
        r, g, b = rgb_str.split(b",")
        return (int(r.strip()), int(g.strip()), int(b.strip()))
    except (ValueError, TypeError):
        return None


class AmbientLight(HomieNode):
    def __init__(self, pin=5, leds=60):
        super().__init__(
            id="ambientlight", name="Ambient Light", type="WS2812B"
        )

        self.np = neopixel.NeoPixel(Pin(pin), leds)

        self.light_property = HomieNodeProperty(
            id="power",
            name="Ambient Light Power",
            settable=True,
            retained=True,
            restore=True,
            datatype="boolean",
            default=FALSE,
        )
        self.add_property(self.light_property)

        self.color_property = HomieNodeProperty(
            id="color",
            name="RGB Color",
            settable=True,
            retained=True,
            restore=True,
            datatype="rgb",
            default=b"254,128,40",
        )
        self.add_property(self.color_property)

    def callback(self, topic, payload, retained):
        if b"power" in topic:
            if payload == TRUE:
                rgb = convert_str_to_rgb(self.color_property.get_data())
                all_on(self.np, color=rgb)
            elif payload == FALSE:
                all_off(self.np)
            else:
                return

            self.light_property.data = payload

        elif b"color" in topic:
            rgb = convert_str_to_rgb(payload)
            if rgb is not None:
                self.color_property.set_data(payload)
                if self.light_property.data == TRUE:
                    all_on(self.np, color=rgb)


def main():
    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(AmbientLight(pin=5, leds=60))

    # run forever
    homie.start()


if __name__ == "__main__":
    main()
