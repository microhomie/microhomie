.. _reference_homie_constants:

:mod:`homie.constants` --- Homie Constants
##########################################

.. module:: homie.constants
   :synopsis: Module for pre-compiled constants


Node property
=============

Datatype
--------

Constants used for datatypes in NodeProperty.

.. data:: STRING
.. data:: ENUM
.. data:: BOOLEAN
.. data:: INTEGER
.. data:: FLOAT
.. data:: COLOR

Format
------
.. data:: RGB
.. data:: HSV


General
=======

Contstants used for payload.

.. data:: ON
.. data:: OFF
.. data:: TRUE
.. data:: FALSE
.. data:: LOCKED
.. data:: UNLOCKED

.. data:: UTF8
.. data:: SET
.. data:: SLASH
.. data:: UNDERSCORE


Device
======

.. data:: QOS

    Homie convention specifies QOS to ``1``.

.. data:: MAIN_DELAY

    This is the delay for the main coro.

.. data:: STATS_DELAY

    This is the delay for the stats coro set to  ``60000``.

.. data:: WDT_DELAY

    Feed the WDT every ``100``ms.

.. data:: DEVICE_STATE

    Name for the subtobic for device state.

Device states
=============

.. data:: STATE_OTA
.. data:: STATE_INIT
.. data:: STATE_READY
.. data:: STATE_RECOVER
.. data:: STATE_WEBREPL


(Sub-) Tobics
=============

.. data:: DEVICE_STATE

    Device state topic ``$state``

.. data:: T_BC

    Homie broadcast topic ``$broadcast``

.. data:: T_MPY

    Microhomie extension topic ``$mpy``

.. data:: T_SET

    ``/set`` topic

Extensions
==========

.. data:: EXT_MPY

    ``org.microhomie.mpy:0.1.0:[4.x]``

.. data:: EXT_FW

    ``org.homie.legacy-firmware:0.1.1:[4.x]``

.. data:: EXT_STATS

    ``org.homie.legacy-stats:0.1.1:[4.x]``
