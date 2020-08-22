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
    def __init__(self, pin, leds):
        super().__init__(id="light", name="Ambient Light", type="WS2812B")
        self._np = neopixel.NeoPixel(Pin(pin), leds)
        self._brightness = 53

        self.p_power = BaseProperty(
            id="power",
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
            on_message=self.on_power_msg,
        )
        self.add_property(self.p_power)

        self.p_color = BaseProperty(
            id="color",
            name="RGB Color",
            settable=True,
            datatype=COLOR,
            default=DEFAULT,
            format=RGB,
            on_message=self.on_color_msg,
        )
        self.add_property(self.p_color)

        self.p_brightness = BaseProperty(
            id="brightness",
            name="Brightness",
            settable=True,
            datatype=ENUM,
            format="1,2,3,4,5,6,7,8",
            default=4,
            on_message=self.on_brightness_msg,
        )
        self.add_property(self.p_brightness)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, val):
        v = min(max(val, 0), 8)
        self._brightness = int(4 + 3.1 * (v + 1) ** 2)

        if self.p_power.value == TRUE:
            rgb = str_to_rgb(self.p_color.value)
            self.on(rgb=rgb)

    def on(self, rgb):
        b = self._brightness
        color = (int(b * rgb[0] / 255), int(b * rgb[1] / 255), int(b * rgb[2] / 255))
        all_on(self._np, color=color)

    def on_power_msg(self, topic, payload, retained):
        if payload == TRUE:
            rgb = str_to_rgb(self.p_color.value)
            self.on(rgb=rgb)
        elif payload == FALSE:
            all_off(self._np)
        else:
            return

        self.p_power.value = payload

    def on_color_msg(self, topic, payload, retained):
        rgb = str_to_rgb(payload)
        if rgb is not None:
            self.p_color.value = payload
            if self.p_power.value == TRUE:
                self.on(rgb=rgb)

    def on_brightness_msg(self, topic, payload, retained):
        try:
            b = min(max(int(payload), 1), 8)
            self.brightness = b
            self.p_brightness.value = payload
        except ValueError:
            pass


def main():
    homie = HomieDevice(settings)

    homie.add_node(
        AmbientLight(
            pin=4,
            leds=3
        )
    )

    homie.run_forever()


if __name__ == "__main__":
    main()
