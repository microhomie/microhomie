.. _reference_homie_utils:

:mod:`homie.utils` --- Homie Utils
##################################

.. module:: homie.utils
   :synopsis: Module for helpers

This module provides a homie value validator.


.. function:: validator.payload_is_valid(cls, payload)

    Validate the payload to the datatype and format defined in the property class.

    The arguments are:

    - ``cls`` property class object
    - ``payload`` the payload to validate
