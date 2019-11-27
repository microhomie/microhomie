.. _reference_homie_utils:

:mod:`homie.utils` --- Homie Utils
##################################

.. module:: homie.utils
   :synopsis: Module for helpers

This module provides helper functions.


.. function:: disable_ap()

    Function to disable the device Wifi Access Point. For the ESP8266 Microhomie firmwares this function will be excecuted on boot.

.. function:: get_unique_id()

    Return a unique device id as bytestring.

.. function:: get_local_ip()

    Return the device IP address, if possible.

.. function:: get_local_mac()

    Return the device MAC address, if possible.

.. function:: payload_is_valid()

    Helper function to validate payload for node properties.

    This function does only test if the payload match the datatype, but the format the payload has to be in, for now.

    Returns ``True`` or ``False``.
