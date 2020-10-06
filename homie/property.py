import uasyncio as asyncio

from homie.constants import STRING, T_SET, TRUE, FALSE
from homie.validator import payload_is_valid


class BaseProperty:
    def __init__(
        self,
        id,
        name=None,
        settable=False,
        retained=True,
        unit=None,
        datatype=STRING,
        format=None,
        default=None,
        restore=True,
        on_message=None,
    ):
        self._value = default

        self.id = id
        self.name = name
        self.settable = settable
        self.retained = retained
        self.unit = unit
        self.datatype = datatype
        self.format = format
        self.restore = restore
        self.on_message = on_message

        self.topic = None
        self.node = None

    # Keep for backward compatibility
    @property
    def data(self):
        return self._value

    # Keep for backward compatibility
    @data.setter
    def data(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """ Set value if changed and publish to mqtt """
        if value != self._value:
            self._value = value
            self.publish()

    def set_topic(self):
        self.topic = "{}/{}/{}".format(
            self.node.device.dtopic,
            self.node.id,
            self.id
        )

    def publish(self):
        asyncio.create_task(
            self.node.device.publish(
                self.topic,
                self.value,
                self.retained
            )
        )

    async def subscribe(self):
        # Restore from topic with retained message on device start
        if self.restore and self.node.device.first_start is True:
            self.node.device.callback_topics[self.topic] = self.restore_handler
            await self.node.device.subscribe(self.topic)

        # Subscribe to settable (/set) topics
        if self.settable is True:
            topic = "{}/set".format(self.topic)
            self.node.device.callback_topics[topic] = self.message_handler
            await self.node.device.subscribe(topic)

    def restore_handler(self, topic, payload, retained):
        """ Gets called when the property should be restored from mqtt """
        # Retained messages are not allowed on /set topics
        if topic.endswith(T_SET):
            return

        # Unsubscribe from topic and remove the callback handler
        asyncio.create_task(self.node.device.unsubscribe(topic))
        del self.node.device.callback_topics[topic]

        if payload_is_valid(self, payload):
            if payload != self._value:
                if self.on_message:
                    self.on_message(topic, payload, retained)

                self._value = payload

    def message_handler(self, topic, payload, retained):
        """ Gets called when the property receive a message on /set topic """
        # No reatained messages allowed on /set topics
        if retained:
            return

        if payload_is_valid(self, payload):
            if self.on_message:
                self.on_message(topic, payload, retained)

            self.value = payload

    async def publish_properties(self):
        topic = self.topic
        publish = self.node.device.publish

        await publish("{}/$name".format(topic), self.name)
        await publish("{}/$datatype".format(topic), self.datatype)

        if self.format is not None:
            await publish("{}/$format".format(topic), self.format)

        if self.settable is True:
            await publish("{}/$settable".format(topic), TRUE)

        if self.retained is False:
            await publish("{}/$retained".format(topic), FALSE)

        if self.unit is not None:
            await publish("{}/$unit".format(topic), self.unit)


HomieProperty = BaseProperty

# Keep for backward compatibility
HomieNodeProperty = BaseProperty
