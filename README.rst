==========
Microhomie
==========

|build-status| |pypi|

A MicroPython implementation of `Homie <https://github.com/homieiot/convention>`_, a lightweight MQTT convention for the IoT. Main target for Microhomie is the ESP8266 device.

Currently Microhomie implements `Homie v3.0.1 <https://github.com/homieiot/convention/releases/tag/v3.0.1>`_.

!Important! Microhomie 1.0.0 (asyncio version) is not compatible with previous 0.3 Microhomie nodes.

Documentation is also outdated, the examples are a good starting point until we update the documentation.


Micropython changes
-------------------

To safe some space we disabled **webrepl** and **btree** support. The AccessPoint SSID is `Microhomie-MAC` with the secret `microhomiE`. You can see all the details in the `micropython.patch` file.


Install
-------

Download the `latest image <https://github.com/microhomie/microhomie/releases>`_ and flash it like any MircoPython image to your ESP8266 device. I.E:

.. code-block:: shell

    esptool --port PORT --baud 460800 write_flash --flash_size=detect --verify -fm dio 0x0 microhomie-esp8266-VERSION.bin

Make your changes in `settings.example.py` and copy this file as `settings.py` to your device. You can now test our example nodes from `examples/`, just copy the `main.py` to your device. Start with the `examples/led` node to turn on and off the on-board LED.


Build image
-----------

To build your own Microhomie image run:

.. code-block:: shell

    make bootstrap
    make requirements
    make
    make flash PORT


Known issues
------------

* SSL connection problems (not tested, with mqtt_as)
