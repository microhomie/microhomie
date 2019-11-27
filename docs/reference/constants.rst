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

.. data:: STATE_INIT
.. data:: STATE_READY
.. data:: STATE_RECOVER


Node
====

.. data:: PUBLISH_DELAY

    This defines the delay for the main publish coro. Set to ``20``.


(Sub-) Tobics
=============

.. data:: T_BC
.. data:: T_SET
