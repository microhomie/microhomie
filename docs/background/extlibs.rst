.. _external_libraries:

External libraries
##################

Microhomie relies on the ``uasyncio`` lib from MicroPython `core libraries <https://github.com/micropython/micropython-lib>`_, the ``mqtt_as.py`` lib from Peter Hinch, patched by Kevin Höck and ``asyn.py`` from Peter Hinch.

To get you startet the ESP8266 firmware has those libs included, plus the ``aswitch.py`` lib from Peter Hinch. If you install Microhomie on ESP32 or other device you can omit the ``aswitch.py`` lib.

``uasyncio``, ``uasyncio.core``, ``mqtt_as.py`` and ``asyn.py`` are requiered for Microhomie.

mqtt_as.py
==========

`mqtt_as.py <https://github.com/peterhinch/micropython-mqtt>`_ is a "resilient" asynchronous non-blocking MQTT driver. In Microhomie we use the `patched <https://github.com/kevinkk525/micropython-mqtt>`_ version from Kevin Köck. Kevins version use keywords to initialize the mqtt_as object, support for "unsubscribe" and support for the unix port of MicroPython.

Author: `Peter Hinch <https://github.com/peterhinch>`_, `Kevin Köck <https://github.com/kevinkk525>`_


asyn.py
=======

`asyn.py <https://github.com/peterhinch/micropython-async/blob/master/asyn.py>`_ 'micro' synchronisation primitives for uasyncio. `asyn` provides Lock, Event, Barrier, Semaphore, BoundedSemaphore, Condition, NamedTask and Cancellable classes, also sleep coro.

Author: `Peter Hinch <https://github.com/peterhinch>`_


aswitch.py
==========

`aswitch.py <https://github.com/peterhinch/micropython-async/blob/master/aswitch.py>`_ Switch and pushbutton classes for asyncio.

.. class:: aswitch.Delay_ms(func=None, args=(), can_alloc=True, duration=1000)

    A retriggerable delay class. Can schedule a coro on timeout.

.. class:: aswitch.Switch(pin)

    Simple debounced switch class for normally open grounded switch.

.. class:: aswitch.Pushbutton(pin, suppress=False)

    Extend the Switch class to support logical state, long press and double-click events

Author: `Peter Hinch <https://github.com/peterhinch>`_
