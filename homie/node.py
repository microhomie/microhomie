import uasyncio as asyncio


class HomieNode:
    def __init__(self, id, name, type):
        self._topic = None
        self.id = id
        self.name = name
        self.type = type
        self.device = None
        self.properties = []

    @property
    def topic(self):
        return self._topic

    def set_topic(self):
        self._topic = "{}/{}".format(
            self.device.dtopic,
            self.id,
        )

    def add_property(self, p, cb=None):
        p.node = self
        self.properties.append(p)

        if cb:
            p.on_message = cb

    async def publish_properties(self):
        """General properties of this node"""
        publish = self.device.publish

        # Publish name and type
        await publish("{}/$name".format(self._topic), self.name)
        await publish("{}/$type".format(self._topic), self.type)

        # Publish properties registerd with the node
        _p = self.properties
        await publish(
            "{}/$properties".format(self._topic),
            ",".join([p.id for p in _p]),
        )

        # Publish registerd properties
        for p in _p:
            await p.publish_properties()

    def broadcast_callback(self, topic, payload, retained):
        """Gets called when the broadcast topic receives a message"""
        pass
