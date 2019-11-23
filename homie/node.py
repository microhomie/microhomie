from homie.constants import FALSE, PUBLISH_DELAY, TRUE, SET, SLASH
from homie.device import await_ready_state
from uasyncio import sleep_ms


class HomieNode:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self._properties = {}

    def add_property(self, p, cb=None):
        if cb:
            p.on_message = cb
        self._properties[p.id] = p

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
            b",".join([pid.encode() for pid in props]),
        )

        for pid, p in props.items():
            t = "{}/{}".format(nid, pid)
            await publish(b"{}/$name".format(t), p.name)
            await publish(b"{}/$datatype".format(t), p.datatype)

            if p.format is not None:
                await publish(b"{}/$format".format(t), p.format)

            if p.settable is True:
                await publish(b"{}/$settable".format(t), TRUE)

            if p.retained is False:
                await publish(b"{}/$retained".format(t), FALSE)

            if p.unit is not None:
                await publish(b"{}/$unit".format(t), p.unit)

    @await_ready_state
    async def publish_data(self):
        nid = self.id
        props = self._properties
        publish = self.device.publish

        while True:
            for pid, p in props.items():
                if p.update is True:
                    data = p._data
                    p.update = False
                    if data is not None:
                        t = b"{}/{}".format(nid, pid)
                        await publish(t, data, p.retained)

            await sleep_ms(PUBLISH_DELAY)

    def callback(self, topic, payload, retained):
        """ Gets called when a payload arrive on node topics

            This method is keeped for backward compatibilty. Old
            Microhomie versions still can overwrite this method in child
            classes to handle mesages.
        """
        t = topic.split(SLASH)
        pid = t.pop()  # property id
        if pid == SET:
            pid = t.pop()

        try:
            p = self._properties[pid.decode()]
            p.msg_handler(topic, payload, retained)
        except KeyError:
            pass

    def broadcast_callback(self, topic, payload, retained):
        """Gets called when the broadcast topic receives a message"""
        pass
