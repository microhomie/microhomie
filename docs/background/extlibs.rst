.. _external_libraries:

External libraries
##################

asyncio primitives
==================

To get you startet the ESP8266 firmware has asyncio primitives from Peter Hinch included

``uasyncio``, ``uasyncio.core``, ``mqtt_as.py`` and ``asyn.py`` are requiered for Microhomie.

switch
------

`switch.py <https://github.com/peterhinch/micropython-async/tree/master/v3/primitives/switch.py>`_ asyncio switch class

.. class:: primitives.switch.Switch(pin)

    Simple debounced switch class for normally open grounded switch.

pushbutton
----------

`pushbutton.py <https://github.com/peterhinch/micropython-async/tree/master/v3/primitives/pushbutton.py>`_ asyncio pushbutton class

.. class:: primitives.pushbutton.Pushbutton(pin, suppress=False)

    Extend the Switch class to support logical state, long press and double-click events

Author: `Peter Hinch <https://github.com/peterhinch>`_


mqtt_as.py
==========

`mqtt_as.py <https://github.com/peterhinch/micropython-mqtt>`_ is a "resilient" asynchronous non-blocking MQTT driver. In Microhomie we use the `patched <https://github.com/kevinkk525/micropython-mqtt>`_ version from Kevin Köck. Kevins version use keywords to initialize the mqtt_as object, support for "unsubscribe" and support for the unix port of MicroPython.

Author: `Peter Hinch <https://github.com/peterhinch>`_, `Kevin Köck <https://github.com/kevinkk525>`_
