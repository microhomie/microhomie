.. _reference_homie_node:

:mod:`homie.node` --- Homie Node
################################

.. module:: homie.node
   :synopsis: Object for Homie node


This module provides an interface to the Homie node definition.


class HomieNode()
=================

The HomieNode object defines the Node as in the Homie convention and should be sub-classed to make nodes. A node must be attached to a Homie device object and can has multiple HomieNodeProperty's. A node object can have multiple property objects.

Usage Model::

    from machine import Pin

    from homie.node import HomieNode
    from homie.constants import FALSE; TRUE, BOOLEAN
    from homie.property import HomieNodeProperty

    # reversed values for the esp8266 boards onboard led
    ONOFF = {FALSE: 1, TRUE: 0, 1: FALSE, 0: TRUE}

    class LEDTestNode(HomieNode):
        def __init__(self, id="led", name="LED test node", type="LED")
            super().__init__(id, name, type)

            # create the esp8266 on-board led object
            self.led = Pin(2, Pin.OUT, value=0)

            # add a homie node property
            self.power_property = HomieNodeProperty(
                id="power",
                name="LED power",
                settable=True,
                datatype=BOOLEAN,
                default=TRUE
            )
            self.add_property(self.power_property, self.on_power_msg)

        def on_power_message(self, topic, payload, retained):
            self.led(ONOFF[payload]
            self.power_property.data = ONOFF[self.led()]

Properties
==========

.. data:: HomieNode.device

    This property will be set to the device object, when a node is registered to the device. With this the methods in the device object can be called from the node object.

Constructor
===========

.. class:: HomieNode(id, name, type)

    Construct a HomieNode object. The arguments are:

        - ``id`` is an unique id for the node.
        - ``name`` is ne human readable node name.
        - ``type`` is the node type.


Methods
=======

.. method:: HomieNode.add_property(self, p, cb=None)

    This method adds HomieNodeProperty objects to the node object. The arguments are:

        - ``p`` is a HomieNodeProperty object.
        - ``cb`` can be an optional message handler that gets called if the property topic receive a message.

.. method:: HomieNode.publish_properties(self)

    This method gets called from the device object on device start and publish all properties registered with the node to MQTT.

    This is an async method.

.. method:: HomieNode.publish_data(self)

    This method will be called from the device object async co-routine for publishing data.

    This is an async method.

.. method:: HomieNode.callback(self, topic, payload, retained)

    This method gets called when a payload arrive for a property registered with the node.

.. method:: HomieNode.broadcast_callback(self, topic, payload, retained)

    This method gets called on any homie broadcast message and should be implemented in the sub-class if the broadcast messages should be handled by the node.
