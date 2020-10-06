==========
Microhomie
==========

|build-status|

Microhomie is a MicroPython framework for `Homie <https://github.com/homieiot/convention>`_, a lightweight MQTT convention for the IoT. Main target for Microhomie is the ESP8266 device and has been well tested and used on ESP32.

Microhomie v3 implements `Homie v4.0.0 <https://github.com/homieiot/convention/releases/tag/v4.0.0>`_.

Read the `Microhomie documentation <https://microhomie.readthedocs.io>`_ to get started.

Learn from our examples until we have a "howto build nodes" section in the documentation or join the #microhomie channel on the `MicroPython Slack community <https://slack-micropython.herokuapp.com/>`_ and chat with us.

Binaries can be verified with `minisign <https://jedisct1.github.io/minisign/>`_ and the following public key:

.. code-block::

    RWTwPeRvouNzP+mcL1t7QDTnKz96i3Kuf95fjpE28szMq8OTycMmiTzX


Update from v2
--------------

Microhomie v3 has some breaking changes you should be aware of before update.

* Microhomie v3 only supports the new LFS2 filesystem. For update you must erase and reflash your device.
* You may need to update your asyncio coroutines as of the new Micropython asyncio v3. Peter Hinch's has a great `asyncio v3 update guide <https://github.com/peterhinch/micropython-async/blob/master/v3/README.md>`_
* New asyncio V3 primitives from Peter Hinch `micropython-async <https://github.com/peterhinch/micropython-async>`_ for switch and pushbutton.
* The ``utils`` module was refactored to ``homie.network``.


MicroPython changes
-------------------

* **btree** and vfat support disabled to save some space
* AccessPoint SSID changed to `Microhomie-MAC` with the secret `microhomiE`
* inisetup.py writes a custom boot.py


Install
-------

Download the `latest image <https://github.com/microhomie/microhomie/releases>`_ and flash it like any MicroPython image to your ESP8266 device. I.E:

.. code-block:: shell

    esptool --port PORT --baud 460800 write_flash --flash_size=detect --verify -fm dio 0x0 microhomie-esp8266-VERSION.bin

Make your changes in ``settings.example.py`` and copy this file as ``settings.py`` to your device. You can now test our example nodes from ``examples/``, just copy the ``main.py`` to your device. Start with the ``examples/led`` node to turn on and off the on-board LED.


Example
-------

This is a basic example to power the on-board LED from an ESP8266 development board:

.. code-block:: python

    import settings

    from machine import Pin

    from homie.node import HomieNode
    from homie.device import HomieDevice
    from homie.property import HomieProperty
    from homie.constants import BOOLEAN, FALSE, TRUE


    # Reversed values map for the esp8266 boards on-board LED
    ONOFF = {FALSE: 1, TRUE: 0}


    # Initialize the pin for the onboard LED
    LED = Pin(2, Pin.OUT, value=1)


    # The on_message handler to power the led
    def toggle_led(topic, payload, retained):
        LED(ONOFF[payload])


    def main():
        # Initialize the Homie device
        device = HomieDevice(settings)

        # Initialize the Homie node for the on-board LED
        led_node = HomieNode(id="led", name="On-board LED", type="LED",)

        # Initialize the Homie property to power on/off the led
        led_power = HomieProperty(
            id="power",
            name="Power",
            settable=True,
            datatype=BOOLEAN,
            default=FALSE,
            on_message=toggle_led,
        )

        # Add the power property to the node
        led_node.add_property(led_power)

        # Add the led node to the device
        device.add_node(led_node)

        # Run
        device.run_forever()


    if __name__ == "__main__":
        main()



Build esp8266 image
-------------------

To build your own Microhomie image for the ESP8266 device, run:


.. code-block:: shell

    make bootstrap
    make
    make deploy PORT=/dev/ttyUSBX


Known issues
------------

* No SSL support for now


.. |build-status| image:: https://readthedocs.org/projects/microhomie/badge/?version=master
    :target: http://microhomie.readthedocs.io/en/master/?badge=master
    :alt: Documentation Status


Included libraries
------------------

* `mqtt_as.py <https://github.com/peterhinch/micropython-mqtt>`_ by Peter Hinch but we use the `patched version <https://github.com/kevinkk525/micropython-mqtt>`_ from Kevin Köck. Kevins version has support for a keyword based configuration and unsubscribe.
* asyncio V3 primitives from Peter Hinch `micropython-async <https://github.com/peterhinch/micropython-async/tree/master/v3>`_ repository.
