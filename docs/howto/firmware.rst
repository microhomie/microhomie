.. _howto_build_firmware:

Build your own Microhomie ESP8266 firmware
##########################################

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
