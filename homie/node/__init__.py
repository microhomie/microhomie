from copy import copy
from utime import time
from uasyncio import sleep_ms


class HomieNodeProperty:
    def __init__(
        self,
        id,
        name=None,
        settable=False,
        retained=True,
        unit=None,
        datatype="string",
        format=None,
        range=0,
        default=None,
    ):
        self.id = id
        self.name = name
        self.settable = settable
        self.retained = retained
        self.unit = unit
        self.datatype = datatype
        self.format = format
        self.range = range
        self._data = [default] * (range + 1)
        self._ldata = [None] * (range + 1)  # last data for delta

    def __repr__(self):
        return "{}(id={!r}, name={!r}, settable={!r}, retained={!r}, unit={!r}, datatype={!r}, format={!r}), range={!r} default={!r}".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.settable,
            self.retained,
            self.unit,
            self.datatype,
            self.format,
            self.range,
            self.default,
        )

    def __str__(self):
        return self.id

    @property
    def data(self):
        return self._data

    def set_data(self, index, val):
        if isinstance(val, bool):
            val = str(val).lower()
        self._data[index] = val


class HomieNode:
    def __init__(self, id, name, type, interval=60):
        self.id = id
        self.name = name
        self.type = type
        self._interval = interval
        self._next_update = time()
        self._properties = []
        self._subscribe = []

    def __repr__(self):
        return "{}(id={!r}, name={!r}, type={!r}, interval={!r})".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.type,
            self._interval,
        )

    def __str__(self):
        """Return nice information about the object"""
        raise NotImplementedError("not implemented")

    def add_property(self, p):
        self._properties.append(p)
        if p.settable:
            self._subscribe.append(b"{}/{}/set".format(self.id, p.id))

            if p.range:
                for i in range(p.range):
                    self._subscribe.append(b"{}/{}/{}/set".format(self.id, p.id, i))

    def has_update(self):
        """Depending on the interval:

        returns True if its time for an update,
        returns False if its not yet time for an update
        """
        if time() > self._next_update:
            self.update_data()
            self._next_update = time() + self._interval
            return True
        return False

    async def get_properties(self):
        """General properties of this node"""
        nid = self.id

        # node attributes
        yield (b"{}/$name".format(nid), self.name)
        yield (b"{}/$type".format(nid), self.type)

        # property attributes
        props = self._properties
        if props:
            yield (
                b"{}/$properties".format(nid),
                b",".join([p.id.encode() for p in props]),
            )

            for p in props:
                t = "{}/{}".format(nid, p.id)
                if p.name:
                    yield (b"{}/$name".format(t), p.name)

                if p.settable:
                    yield (b"{}/$settable".format(t), b"true")

                if p.retained is False:
                    yield (b"{}/$retained".format(t), b"false")

                if p.unit:
                    yield (b"{}/$unit".format(t), p.unit)

                if p.datatype != "string":
                    yield (b"{}/$datatype".format(t), p.datatype)

                if p.datatype in ["enum", "color"]:
                    yield (b"{}/$format".format(t), p.format)

    async def publish_data(self, client):
        nid = self.id
        props = self._properties
        while True:
            if self.has_update():
                for p in props:
                    data = p.data
                    ldata = p._ldata  # last data
                    r = range(len(data))
                    for i in r:
                        if data[i] is not None:
                            if data[i] == ldata[i]:
                                continue
                            t = b"{}/{}".format(nid, p.id)
                            if i > 0:
                                t += b"/{}".format(i - 1)
                            await client.publish(t, data[i], p.retained)

                    p._ldata = copy(data)

            await sleep_ms(100)

    def update_data(self):
        """Prepare new data. Measure nodes... """
        raise NotImplementedError("not implemented")

    def callback(self, topic, payload, retained):
        """Gets called when self.subscribe has topics"""
        raise NotImplementedError("not implemented")

    def broadcast_callback(self, topic, payload, retained):
        """Gets called when the broadcast topic receives a message"""
        pass

    def get_property_id_from_set_topic(self, topic):
        """Return the property id from topic as integer"""
        retval = None
        try:
            return int(topic.split(b"/")[-3].split(b"_")[-1])
        except (TypeError, ValueError):
            pass
        return retval
