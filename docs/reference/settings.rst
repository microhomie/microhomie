.. _reference_homie_settings:

:mod:`settings` --- Homie Settings
##################################

.. module:: settings
   :synopsis: Module to configure Microhomie

This module is to configure the home device. For reference see the example settings file in the repository.


Mandatory
=========

All mandatory settings must be set in the settings.py config file on the device.

Wifi settings
-------------

.. data:: WIFI_SSID

    SSID for the wifi to connect with. Value must be string.

.. data:: WIFI_PASSWORD

    The password for the wifi to connect with. Value must be string.


MQTT settings
-------------

.. data:: MQTT_BROKER

    The MQTT broker IP address or hostname. Value must be string.


Optional
========

Optional settings have a default value an can be overwritten in the settings file.

Debug
-----

.. data:: DEBUG

    Set DEBUG to ``True`` to enable debug log output and to disable the WDT. Default ist ``False``.

MQTT settings
-------------

.. data:: MQTT_PORT

    Default port is ``1883``. Value must be integer.

.. data:: MQTT_USERNAME

    The username to connect with. Default is ``None``. Value must be string.

    Do not set username for anonymouse auth.

.. data:: MQTT_PASSWORD

    The password for the username to connect with. Default is ``None``. Value must be string.

.. data:: MQTT_KEEPALIVE

    Default keepalive in seconds is ``30``. Value must be interger.

.. data:: MQTT_SSL

    My only work on ESP32. Default is ``False``. Set to ``True`` to enable SSL.

.. data:: MQTT_SSL_PARAMS

    Aditional SSL params as dict(). Default is set to ``{"do_handshake": True}``.

.. data:: MQTT_BASE_TOPIC

    The base topic for the homie device. Default is ``b"homie"``. Value must be bytestring.

Device settings
---------------

.. data:: DEVICE_ID

    The device ID for registration at the broker. The device id is also the base topic of the device and must be unique. Default is to use a generated ID, hex encoded as bytestring: ``homie.utils.get_unique_id()``.

    Value must be bytestring and unique.

.. data:: DEVICE_NAME

    Friendly name of the device. Value must be bytestring.

.. data:: DEVICE_STATS_INTERVAL

    Time in seconds the stats coro publish updates. Default is 60 seconds.

Extensions
----------

.. data:: EXTENSIONS

    Default is a empty list() for no extensions. Microhomie currently supports two legacy extensions. Add the extensions to the list to activate them. Items in the list() must be bytestring.

    * org.homie.legacy-firmware:0.1.1:[4.x]
    * org.homie.legacy-stats:0.1.1:[4.x]

    Example::

        EXTENSIONS = [
            b"org.homie.legacy-firmware:0.1.1:[4.x]",
            b"org.homie.legacy-stats:0.1.1:[4.x]",
        ]
