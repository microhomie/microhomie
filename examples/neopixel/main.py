import neopixel
import settings

from machine import Pin

from homie.node import HomieNode
from homie.device import HomieDevice
from homie.property import HomieNodeProperty
from homie.constants import TRUE, FALSE, BOOLEAN, COLOR, RGB, ENUM


BLACK = (0, 0, 0)

DEFAULT = "159,5,0"


def all_off(np):
    np.fill(BLACK)
    np.write()


def all_on(np, color=DEFAULT):
    np.fill(color)
    np.write()


def convert_str_to_rgb(rgb_str):
    try:
        r, g, b = rgb_str.split(",")
        return (int(r.strip()), int(g.strip()), int(b.strip()))
    except (ValueError, TypeError):
        return None


class AmbientLight(HomieNode):
    def __init__(self, pin=5, leds=3):
        super().__init__(
            id="light", name="Ambient Light", type="WS2812B"
        )
        self._brightness = 53

        self.np = neopixel.NeoPixel(Pin(pin), leds)

        self.power_property = HomieNodeProperty(
            id="power",
            name="Light power",
            settable=True,
            retained=True,
            restore=True,
            datatype=BOOLEAN,
            default=FALSE,
        )
        self.add_property(self.power_property, self.on_power_msg)

        self.color_property = HomieNodeProperty(
            id="color",
            name="RGB Color",
            settable=True,
            retained=True,
            restore=True,
            datatype=COLOR,
            default=DEFAULT,
            format=RGB,
        )
        self.add_property(self.color_property, self.on_color_msg)

        self.brightness_property = HomieNodeProperty(
            id="brightness",
            name="LED brightness",
            settable=True,
            retained=True,
            restore=True,
            datatype=ENUM,
            format="1,2,3,4,5,6,7,8",
            default=4,
        )
        self.add_property(self.brightness_property, self.on_brightness_msg)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, val):
        v = min(max(val, 0), 8)
        self._brightness = int(4 + 3.1 * (v + 1) ** 2)

        if self.power_property.data == TRUE:
            rgb = convert_str_to_rgb(self.color_property.data)
            self.on(rgb=rgb)

    def on(self, rgb):
        b = self._brightness
        color = (
            int(b * rgb[0] / 255),
            int(b * rgb[1] / 255),
            int(b * rgb[2] / 255)
        )
        all_on(self.np, color=color)

    def on_power_msg(self, topic, payload, retained):
        if payload == TRUE:
            rgb = convert_str_to_rgb(self.color_property.data)
            self.on(rgb=rgb)
        elif payload == FALSE:
            all_off(self.np)
        else:
            return

        self.power_property.data = payload

    def on_color_msg(self, topic, payload, retained):
        rgb = convert_str_to_rgb(payload)
        if rgb is not None:
            self.color_property.data = payload
            if self.power_property.data == TRUE:
                self.on(rgb=rgb)

    def on_brightness_msg(self, topic, payload, retained):
        try:
            b = min(max(int(payload), 1), 8)
            self.brightness = b
            self.brightness_property.data = payload
        except ValueError:
            pass


def main():
    homie = HomieDevice(settings)
    homie.add_node(AmbientLight())
    homie.run_forever()


if __name__ == "__main__":
    main()
