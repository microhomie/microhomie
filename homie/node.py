from homie.constants import FALSE, PUBLISH_DELAY, SLASH, TRUE, UNDERSCORE
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
        if props:
            await publish(
                b"{}/$properties".format(nid),
                b",".join([p.id.encode() for p in props]),
            )

            for p in props:
                t = "{}/{}".format(nid, p.id)
                if p.name:
                    await publish(b"{}/$name".format(t), p.name)

                if p.range > 1:
                    await publish(
                        b"{}/$array".format(t), b"0-{}".format(p.range - 1)
                    )

                if p.settable:
                    await publish(b"{}/$settable".format(t), TRUE)

                if p.retained is False:
                    await publish(b"{}/$retained".format(t), FALSE)

                if p.unit:
                    await publish(b"{}/$unit".format(t), p.unit)

                if p.datatype != "string":
                    await publish(b"{}/$datatype".format(t), p.datatype)

                if p.datatype in ["enum", "color"]:
                    await publish(b"{}/$format".format(t), p.format)

    @await_ready_state
    async def publish_data(self):
        nid = self.id
        props = self._properties
        publish = self.device.publish

        while True:
            for p in props:
                if p._update is True:
                    p._update = False

                    delta = p._delta

                    is_array = p.range > 1
                    for i, data in enumerate(p):
                        if data is not None:
                            if data == delta[i] and is_array:
                                continue

                            if is_array:
                                t = b"{}_{}/{}".format(nid, i, p.id)
                            else:
                                t = b"{}/{}".format(nid, p.id)

                            await publish(t, data, p.retained)

                    if p.retained:
                        p.update_delta()

            await sleep_ms(PUBLISH_DELAY)

    def callback(self, topic, payload, retained):
        """Gets called when self.subscribe has topics"""
        raise NotImplementedError("not implemented")

    def broadcast_callback(self, topic, payload, retained):
        """Gets called when the broadcast topic receives a message"""

    def get_array_id_from_set_topic(self, topic):
        """Return the id from an array property topic as integer"""
        levels = topic.split(SLASH)
        for l in levels:
            if UNDERSCORE in l:
                try:
                    return int(l.split(UNDERSCORE)[-1])
                except ValueError:
                    pass

    def get_property_id_from_set_topic(self, topic):
        # deprecated - will be removed in future
        return self.get_array_id_from_set_topic(topic)
