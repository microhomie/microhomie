========================================
Example code for Gosund SP1 Power Socket
========================================

This example code can switch the relay on and off via MQTT or the button on the top. Long press on the button will reset the device.

Blue LED = power off
Red LED = power on

https://www.amazon.de/gp/product/B0777BWS1P

Gosund must be flashed with ``-fm dout`` to acceess the repl.

.. code-block:: shell

    esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dout 0x0 micropython/ports/esp8266/build/firmware-combined.bin

TODO
----

 * Add Support for power monitoring chip
