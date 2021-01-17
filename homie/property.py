import uasyncio as asyncio

from homie.constants import STRING, T_SET, TRUE, FALSE, SLASH
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
        pub_on_upd=True,
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
        self.pub_on_upd = pub_on_upd

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
        """Assign new value if changed or self.pub_on_upd is True and publish to mqtt"""
        if value != self._value:
            self._value = value
            self.publish()
        elif self.pub_on_upd:
            self.publish()

    def set_topic(self):
        self.topic = "{}/{}/{}".format(
            self.node.device.dtopic,
            self.node.id,
            self.id
        )

    def publish(self):
        if self._value is None:
            return

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


def get_index_from_set_topic(topic):
    levels = topic.split(SLASH)
    levels.reverse()
    for l in levels:
        try:
            return int(l)
        except ValueError:
            pass


class ArrayProperty(BaseProperty):
    def __init__(
        self,
        id,
        array,
        name=None,
        settable=False,
        retained=True,
        restore=True,
        unit=None,
        datatype=STRING,
        format=None,
        default=None,
        on_message=None,
        pub_on_upd=True,
    ):
        super().__init__(
            id,
            name,
            settable,
            retained,
            unit,
            datatype,
            format,
            default,
            restore,
            on_message,
            pub_on_upd,
        )
        self._array = array
        self._value = [default] * array

    def __len__(self):
        return len(self._value)

    def __iter__(self):
        for d in self._value:
            yield d

    def __contains__(self, i):
        if i in self._value:
            return True
        return False

    def __getitem__(self, i):
        return self._value[i]

    def __setitem__(self, k, v):
        try:
            if v != self._value[k]:
                self._value[k] = v
                self.publish_id(k)
            elif self.pub_on_upd:
                self.publish_id(k)
        except IndexError as err:
            self.node.device.dprint("ERROR:ArrayProperty: IndexError: {}".format(err))

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, value):
        raise NotImplementedError

    def set_topic(self):
        self.topic = "{}/{}".format(
            self.node.device.dtopic,
            self.node.id
        )

    def get_topic(self, aid):
        return "{}/{}/{}".format(self.topic, aid, self.id)

    async def publish(self):
        r = range(0, self._array)
        for i in r:
            self.publish_id(i)

    def publish_id(self, aid):
        if self._value[aid] is None:
            return

        asyncio.create_task(
            self.node.device.publish(
                self.get_topic(aid),
                self._value[aid],
                self.retained
            )
        )

    async def subscribe(self):
        # Restore from topic with retained message on device start
        topic = "{}/+/{}".format(self.topic, self.id)
        if self.restore and self.node.device.first_start is True:
            self.node.device.callback_topics[topic] = self.restore_handler
            await self.node.device.subscribe(topic)

        # Subscribe to settable (/set) topics
        if self.settable is True:
            pset_topic = "{}/{}/set".format(self.topic, self.id)
            self.node.device.callback_topics[pset_topic] = self.message_handler
            await self.node.device.subscribe(pset_topic)

            set_topic = "{}/set".format(topic)
            self.node.device.callback_topics[set_topic] = self.message_handler
            await self.node.device.subscribe(set_topic)

    def restore_handler(self, topic, payload, retained):
        """ Gets called when the property should be restored from mqtt """
        # Retained messages are not allowed on /set topics
        if topic.endswith(T_SET):
            return

        if payload_is_valid(self, payload):
            index = get_index_from_set_topic(topic)

            if payload != self._value[index]:
                if self.on_message:
                    self.on_message(topic, payload, retained)

                self._value[index] = payload

    def message_handler(self, topic, payload, retained):
        """ Gets called when the property receive a message on /set topic """
        # No reatained messages allowed on /set topics
        if retained:
            return

        if payload_is_valid(self, payload):
            if self.on_message:
                self.on_message(topic, payload, retained)

            index = get_index_from_set_topic(topic)

            if index:
                self[index] = payload


# Keep for backward compatibility
HomieProperty = BaseProperty
HomieNodeProperty = BaseProperty
