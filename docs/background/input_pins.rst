.. _input_pins:

Recommended input pins
######################

Recommended ESP8266 input pins
==============================

The following ESP8266 GPIO pins are recommended for as input pins.

* GPIO4
* GPIO5
* GPIO12
* GPIO13
* GPIO14
* GPIO16

The following ESP8266 GPIO pins should be used with caution. There is a risk that the state of the pins can affect the boot sequence. When possible, use other GPIO pins.

* GPIO0 - used to detect boot-mode.  Bootloader runs when pin is low during powerup.
* GPIO2 - used to detect boot-mode.  Attached to pull-up resistor.
* GPIO15 - used to detect boot-mode.  Attached to pull-down resistor.

One pin does not support interrupts.

* GPIO16 - does not support interrupts.


Recommended ESP32 input pins
============================

The following ESP32 GPIO pins should be used with caution. There is a risk that the state of the pins can affect the boot sequence. When possible, use other GPIO pins.

* GPIO0 - used to detect boot-mode.  Bootloader runs when pin is low during powerup. Internal pull-up resistor.
* GPIO2 - used to enter serial bootloader.  Internal pull-down resistor.
* GPIO4 - technical reference indicates this is a strapping pin, but usage is not described.  Internal pull-down resistor.
* GPIO5 - used to configure SDIO Slave.  Internal pull-up resistor.
* GPIO12 - used to select flash voltage.  Internal pull-down resistor.
* GPIO15 - used to configure silencing of boot messages.  Internal pull-up resistor.
