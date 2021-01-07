========================================
Example code for Gosund SP1 Power Socket
========================================

This example code can switch the relay on and off via MQTT or the button on the top. Long press on the button will reset the device.

Blue LED = power off
Red LED = power on

https://www.amazon.de/gp/product/B0777BWS1P

The Gosund Power Socket ESP8266 has 1MB Flash size. Build your Microhomie as follows to get a Firmware for 1MB flash size devices. The 1MB version does not include uasyncio.

Add ``#define MICROPY_PY_UASYNCIO             (1)`` to the ``ports/esp8266/boards/GENERIC_1M/mpconfigboard.h`` file.

And build the firmware:

.. code-block:: shell

    make BOARD=GENERIC_1M


Gosund must be flashed with ``-fm dout`` to acceess the repl.

.. code-block:: shell

    esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dout 0x0 releases/microhomie-esp8266-vX.X.X.bin


TODO
----

 * Add Support for power monitoring chip
