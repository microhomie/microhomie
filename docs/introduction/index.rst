.. _introduction:

.. toctree::
    :maxdepth: 1

Get Started
###########

First steps to understand Microhomie and get to know it.

.. note:: If you just started with MicroPython, a good start is the `Getting started with MicroPython on the ESP8266 <http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html>`_ tutorial from the MicroPython documentation.

Prepare MQTT
============

Checkout mosquitto MQTT Server (https://mosquitto.org) if you want to host a server yourself or head over to IO Adafruit (https://io.adafruit.com), create an account and use their MQTT API (https://learn.adafruit.com/adafruit-io/mqtt-api).


Install Microhomie on the ESP8266
=================================

The first thing you need to do is to load the Microhomie firmware, a modified MicroPython firmware, onto your ESP8266 device.

You can download the Microhomie firmware from the `GitHub release page <https://github.com/microhomie/microhomie/releases>`_ and flash it like any MircoPython firmware to your ESP8266 device. I.E:

.. code-block:: shell

    esptool --port PORT --baud 460800 write_flash --flash_size=detect --verify -fm dio 0x0 microhomie-esp8266-v2.2.0.bin

Continue with the `configuration`_ and the `Quick start with a simple LED node`_ sections.


Install Microhomie on the ESP32
===============================

Install MicroPython
-------------------

For now, follow this tutorial (https://www.cnx-software.com/2017/10/16/esp32-micropython-tutorials/) to install MicroPython on the ESP. Please remember to use the latest version of the ESP software during the installation.

Get the latest `firmware for ESP32 boards <https://micropython.org/download#esp32>`_.

.. important::  On some boards, the installation of MicroPython will fail with an "connection timeout" if you have any wires attached to the board. This depends on your board and you have to detach all wires except power for the basic installation to work. This is only relevant for the installation of MicroPython and not Microhomie.

Once the installation is successful and you are able to execute python code on the ESP32, you can install Microhomie.

Install Microhomie
------------------

For the ESP32 you can just copy Microhomie with all requirements to your device.

Clone the Microhomie repository:

.. code-block:: shell

    git clone https://github.com/microhomie/microhomie.git

and copy ``lib`` and ``homie`` from your host to the device. ``homie`` should be copied to the device ``lib`` directory:

.. code-block:: shell

    lib/
    ├── aswitch.py
    ├── asyn.py
    ├── homie
    │   ├── constants.py
    │   ├── device.py
    │   ├── __init__.py
    │   ├── node.py
    │   ├── property.py
    │   └── utils.py
    ├── mqtt_as.py
    └── uasyncio
        ├── core.py
        └── __init__.py


For example we have an `mpfshell <https://github.com/wendlers/mpfshell>`_ script ``esp32_install.mpf`` to automate the deployment:

.. code-block:: shell

    mpfshell ttyUSB0 -s esp32_install.mpf

Continue with the `configuration`_ and the `Quick start with a simple LED node`_ sections.


Configuration
=============

To configure your Microhomie device create a ``settings.py`` file from the ``settings.example.py`` file, make your changes and copy the file to your ESP8266 device.

Reference: :ref:`reference_homie_settings`


Quick start with a simple LED node
==================================

The LED example in this guide use the on-board LED, so you don't need to do any wiring to get started.

Copy the ``main.py`` file from the ``examples/led`` directory to your ESP8266, reset the device and watch the incoming MQTT messages.

If everything is setup correctly, the data will then be pushed to the MQTT server in the homie format. Take a look at the homie specification (https://homieiot.github.io/specification/#) to get an idea of the possibilities.

::

    homie/2fe65700/$homie 4.0.0
    homie/2fe65700/$name LED test
    homie/2fe65700/$state init
    homie/2fe65700/$implementation esp8266
    homie/2fe65700/$nodes led
    homie/2fe65700/led/$name Onboard LED
    homie/2fe65700/led/$type LED
    homie/2fe65700/led/$properties power
    homie/2fe65700/led/power/$name LED Power
    homie/2fe65700/led/power/$datatype boolean
    homie/2fe65700/led/power/$settable true
    homie/2fe65700/$extensions org.homie.legacy-firmware:0.1.1:[4.x],org.homie.legacy-stats:0.1.1:[4.x]
    homie/2fe65700/$localip 10.42.0.3
    homie/2fe65700/$mac 80:7d:3a:bb:c7:8a
    homie/2fe65700/$fw/name Microhomie
    homie/2fe65700/$fw/version 2.2.0
    homie/2fe65700/$stats/interval 60
    homie/2fe65700/led/power true
    homie/2fe65700/$stats/uptime 0
    homie/2fe65700/$stats/freeheap 15520
    homie/2fe65700/$state ready

To turn the on-board LED from your ESP8266 on or off send ``true`` or ``false`` to the property topic. For example:

.. code-block:: shell

    mosquitto_pub -h HOST -u USER -P PASSWORD --qos 1 -t "homie/DEVICE-ID/led/power/set" -m false
