========================
Microhomie documentation
========================

Welcome! This is the documentation for Microhomie v1.0.0.

Microhomie is a `MicroPython <https://micropython.org>`_ framework for `Homie <https://github.com/homieiot/convention>`_, a lightweight MQTT convention for the IoT.

The main target device is the ESP8266.


Install Microhomie on the ESP8266
---------------------------------

The first thing you need to do is to load the Microhomie firmware, a modified MicroPython firmware, onto your ESP8266 device. You can download the firmware from the `GitHub release page <https://github.com/microhomie/microhomie/releases>`_.

If you just started with MicroPython, a good start is the `Getting started with MicroPython on the ESP8266 <http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html>`_ from the MicroPython documentation.


Configuration
-------------

To configure your Microhomie device create a ``settings.py`` file from the ``settings.example.py`` file, make your changes and copy the file to your ESP8266 device.


Get started with a simple LED node
----------------------------------

The LED example in this guide use the on-board LED, so you don't need to do any wiring to get started.

Copy the ``main.py`` file from the ``examples/led`` directory to your ESP8266, reset the device and watch the incoming MQTT messages.

To turn the on-board LED from your ESP8266 on or off send ``true``, ``false`` or ``toggle`` to the property topic. For example:

.. code-block:: shell

    mosquitto_pub -h HOST -u USER -P PASSWORD -t "homie/DEVICE-ID/led/power/set" -m true


Build your own Microhomie ESP8266 firmware
------------------------------------------

If you want to build your own Microhomie firmware, maybe for helping us with development, learning or just for the fun to build your own firmware, follow the next steps.

First clone the Microhomie repository:

.. code-block:: shell

    git clone https://github.com/microhomie/microhomie.git

The next step is to setup the build environment, build the `esp-open-sdk <https://github.com/pfalcon/esp-open-sdk>`_ (`Requirements and Dependencies <https://github.com/pfalcon/esp-open-sdk#requirements-and-dependencies>`_), get the MicroPython source, prepare it for the Microhomie firmware and download the required MicroPython modules:

.. code-block:: shell

    cd microhomie
    make bootstrap

Now you can build your Microhomie firmware and load it to your ESP8266:

.. code-block:: shell

    make

Erase and flash:

.. code-block:: shell

    make delpoy PORT=/dev/ttyUSBX

Just flash:

.. code-block:: shell

    make flash PORT=/dev/ttyUSBX

If you want to help with development, please use our linting:

.. code-block:: shell

    make lint
