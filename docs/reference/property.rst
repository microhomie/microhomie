.. _reference_homie_property:

:mod:`homie.property` --- Homie Node Property
#############################################

.. module:: homie.property
   :synopsis: Object for Homie Node Properties


This module provides an interface to the Homie Node Property definition.


class HomieNodeProperty()
=========================

A property object is used to define a homie node property. A property object
must be attached to a node object.

Usage Model::

    from homie.constants import ENUM, FALSE

    from homie.property import HomieNodeProperty

    power_property = HomieNodeProperty(
        id="power",
        name="Power",
        settable=True,
        datatype=BOOLEAN,
        default=TRUE,
    )


Constructor
===========

.. class:: HomieNodeProperty(id, name=None, settable=False, retained=True, unit=None, datatype=STRING, format=None, default=None, restore=True)

    The arguments id, name, settable, retained, unit, datatype and format are arguments from the Homie convention definition for `property attributes <https://homieiot.github.io/specification/#property-attributes>`_ with the same defaults.

    The arguments default and restore are Microhomie specific.

    The arguments are:

      - ``id`` is mandatory and must be a unique property ID on a per-node basis.
      - ``name`` specifies the a friendly name of the property.
      - ``settable`` allows a property to be settable and enables the /set topic. Default is False.
      - ``retained`` specifies if the property is a retained message. Default is True.
      - ``unit`` optional unit of this proeprty.
      - ``datatype`` specifies the data type as byte string. Allowed data types are string, integer, float, boolean, enum, color. This types can be importet from `homie.constants`. Default is STRING.
      - ``format`` specifies restrictions or options for the given data type. Default is None.

        - For integer and float: Describes a range of payloads e.g. 10:15
        - For enum: payload,payload,payload for enumerating all valid payloads.
        - For color:
            - ``rgb`` to provide colors in RGB format e.g. 255,255,0 for yellow.
            - ``hsv`` to provide colors in HSV format e.g. 60,100,100 for yellow.

      - ``default`` set the default message payload. Default is None.
      - ``restore`` restore property payload from mqtt retained message. Default is True.


Properties
==========

.. data:: HomieNodeProperty.data

  This is where the property data/payload is stored.


Methods
=======

.. method:: HomieNodeProperty.msg_handler(self, topic, payload, retained)

    This method handles incoming payload for the property. Per default this method validates the payload and updates the object data with the new payload.

    To overwrite the default handler set a `on_message` handler when adding the property to the node. See HomieNode.add_property().

    The arguments are:

    - ``topic`` the message topic.
    - ``payload`` the message payload.
    - ``retained`` specifies if the payload is retained.


Useful constants
================

The following constants can be used for the `datatype` argument.

.. data:: homie.constants.STRING
          homie.constants.BOOLEAN
          homie.constants.INTEGER
          homie.constants.FLOAT
          homie.constants.ENUM
          homie.constants.COLOR
