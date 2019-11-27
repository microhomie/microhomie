.. _reference_homie_device:

:mod:`homie.device` --- Homie Device
####################################

.. module:: homie.device
   :synopsis: Module for Homie device


This module provides an interface to the Homie device definition.

Consider to read the Homie convention for details.


Decorator
=========

.. function:: await_ready_state(func)

    Is an async decorator to block async coros as long as the device has published all device topics and announced itself as ready.

    Decorate methods with this if the method should wait until the device is ready.


class HomieDevice()
===================

The HomieDevice object is the core that handles all incoming and outgoing messages in the way the homie convention is defined.

One HomieDevice object can have multiple HomieNode objects. Microhomie can run with only the device object without nodes but the homie convention requires as minimum one node per device.

Usage Model::

    import settings

    from mynode import MyNode
    from homie.node import HomieNode


    homie = HomieDevice(settings)
    homie.add_node(MyNode)
    homie.run_forever()


Constructor
===========

.. class:: HomieDevice(settings)

    Construct a Homie device object. The arguments are:

        - ``settings`` is the settings module from the settings.py file.

Methods
=======

.. method:: HomieDevice.add_node(self, node)

    This method is used to register a HomieNode object to the device.

    The arguments are:

        - ``node`` is the HomieNode object.

.. method:: HomieDevice.format_topic(self, topic)

    This method returns a string with the given topic and the precedent topic from the device.

    The arguments are:

        - ``topic`` is the sub topic i.e. from a node or property that should be precedent with the device topic.

.. method:: HomieDevice.subscribe(self, topic)

    This method subscribes to the given topic.

    The arguments are:

        - ``topic`` is the topic that should be subscribed to.


.. method:: HomieDevice.unsubscribe(self, topic)

    This method is used to unsubscribe a topic.

    The arguments are:

        - ``topic`` is the topic that should be unsubscribed.

.. method:: HomieDevice.add_node_cb(self, node)

    This method is used internal the device object to add the node callback method to a dictionary.

    The arguments are:

        - ``node`` is a HomieNode object.

.. method:: HomieDevice.connection_handler(self, client)

    Internal method that gets called when the mqtt connection is established. This method subscribes to all the topics, handle data restore and finaly register the coroutines to send data.

    The arguments are:

        - ``client`` is the mqtt_as client object.

.. method:: HomieDevice.sub_cb(self, topic, payload, retained)

    This method is the base callback method for arriving messages. Every message arrives on a subscribed topic calls this method.

    This method test if the topic is a broadcast topic and pass the message to all nodes broadcast_callback method.

    Else the payload should be passed to the node that has subscribed to the messages topic.

    The arguments are:

        - ``topic`` is the topic the message has arrived on.
        - ``payload`` is a binary string with the message payload.
        - ``retained`` indicates if the messages is retained on the broker.

.. method:: HomieDevice.publish(self, topic, payload, retained=True)

    This method is used to publish data. Topics will be prefixed with the device base topic.

    The arguments are:

        - ``topic`` the sub-topic the payload should be published to.
        - ``payload`` is the payload.
        - ``retained`` indicates if the message should be retained on the broker. Convention default is True.

.. method:: HomieDevice.broadcast(self, payload, level=None)

    This method can be used to send payload to the Homie broadcast topic. If the level argument is not None, it will be attached as a sub-topic to the broadcast topic.

    The arguments are:

        - ``payload`` the payload to send.
        - ``level`` is the broadcast level for the payload. Default is no level.

.. method:: HomieDevice.publish_properties(self)

    This method publish the device properties as defined in the Homie convention.


.. method:: HomieDevice.publish_stats(self)

    This is a async coroutine to publish device stats.

.. method:: HomieDevice.run(self)

    This method is the main loop. It handles the mqtt connection and tries to reconnect if there is an error.

.. method:: HomieDevice.run_forever(self)

    This method should be called from main to start the device.

.. method:: HomieDevice.wdt(self):

    This method is a loop that feeds a watch dog timer. To disable the WDT set DEBUG to True in the settings.py file.

.. method:: HomieDevice.dprint(self)

    This method will print to stdout if DEBUG is enabled.


