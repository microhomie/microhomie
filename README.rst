==========
Microhomie
==========

|build-status|

A MicroPython implementation of `Homie <https://github.com/homieiot/convention>`_, a lightweight MQTT convention for the IoT. Main target for Microhomie is the ESP8266 device.

Currently Microhomie implements `Homie v3.0.1 <https://github.com/homieiot/convention/releases/tag/v3.0.1>`_.

The `Homie v4.0.0 <https://github.com/homieiot/convention/releases/tag/v4.0.0>`_ version is currently in beta. Code is in `develop <https://github.com/microhomie/microhomie/tree/develop>`_ branch and we have pre-build `images <https://github.com/microhomie/microhomie/releases>`_.

**Important** Microhomie 1.0.0 (asyncio version) is not compatible with previous 0.3 Microhomie nodes.

Read the `Microhomie documentation <https://microhomie.readthedocs.io>`_ to get started. If you want to make your own node, learn from our examples until we have a "howto build nodes" section in the documentation or get in contact with us on `Slack <https://join.slack.com/t/microhomie/shared_invite/enQtMzA3MTIwNTg3OTU4LTdjMmQxNGI1ZTIzN2IwZjNiMDRkMDE4NGM3Mjc3MWE4ZWUxNzdhOTVhZWIxYmNiZDBjZDlhMTY2MmIyOGZiODI>`_.

Binaries can be verified with `minisign <https://jedisct1.github.io/minisign/>`_ and the following public key:

.. code-block::

    RWTwPeRvouNzP+mcL1t7QDTnKz96i3Kuf95fjpE28szMq8OTycMmiTzX

Join the #microhomie channel on the `MicroPython Slack community <https://slack-micropython.herokuapp.com/>`_.


MicroPython changes
-------------------

To save some space we disabled **webrepl** and **btree** support. The AccessPoint SSID is `Microhomie-MAC` with the secret `microhomiE`. You can see all the details in the `micropython.patch` file.


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
    make
    make delpoy PORT=/dev/ttyUSBX


Known issues
------------

* No SSL support for now


.. |build-status| image:: https://readthedocs.org/projects/microhomie/badge/?version=master
    :target: http://microhomie.readthedocs.io/en/master/?badge=master
    :alt: Documentation Status
