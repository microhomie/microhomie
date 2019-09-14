from homie.constants import FALSE, PUBLISH_DELAY, TRUE
from homie.device import await_ready_state
from uasyncio import sleep_ms


class HomieNode:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self._properties = []

    def add_property(self, p):
        self._properties.append(p)

    async def publish_properties(self):
        """General properties of this node"""
        nid = self.id
        publish = self.device.publish

        # node attributes
        await publish(b"{}/$name".format(nid), self.name)
        await publish(b"{}/$type".format(nid), self.type)

        # property attributes
        props = self._properties
        await publish(
            b"{}/$properties".format(nid),
            b",".join([p.id.encode() for p in props]),
        )

        for p in props:
            t = "{}/{}".format(nid, p.id)
            await publish(b"{}/$name".format(t), p.name)
            await publish(b"{}/$datatype".format(t), p.datatype)

            if p.format is not None:
                await publish(b"{}/$format".format(t), p.format)

            if p.settable is True:
                await publish(b"{}/$settable".format(t), TRUE)

            if p.retained is False:
                await publish(b"{}/$retained".format(t), FALSE)

            if p.unit:
                await publish(b"{}/$unit".format(t), p.unit)

    @await_ready_state
    async def publish_data(self):
        nid = self.id
        props = self._properties
        publish = self.device.publish

        while True:
            for p in props:
                if p._update is True:
                    data = p._data
                    p._update = False
                    if data is not None:
                        t = b"{}/{}".format(nid, p.id)
                        await publish(t, data, p.retained)

            await sleep_ms(PUBLISH_DELAY)

    def callback(self, topic, payload, retained):
        """Gets called when self.subscribe has topics"""
        raise NotImplementedError("not implemented")

    def broadcast_callback(self, topic, payload, retained):
        """Gets called when the broadcast topic receives a message"""
