from utime import time


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
    ):
        self.id = id
        self.name = name
        self.settable = settable
        self.retained = retained
        self.unit = unit
        self.datatype = datatype
        self.format = format
        self._data = None

    def __repr__(self):
        return "{}(id={!r}, name={!r}, settable={!r}, retained={!r}, unit={!r}, datatype={!r}, format={!r})".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.settable,
            self.retained,
            self.unit,
            self.datatype,
            self.format,
        )

        def __str__(self):
            return self.id

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, val):
            if isinstance(val, bool):
                val = str(val).lower()
            self._data = val


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
            self._subscribe.append(
                b"{}/{}/set".format(self.id, p.id,)
            )

    def subscribe(self):
        for t in self._subscribe:
            yield t

    def has_update(self):
        """Depending on the interval:

        returns True if its time for an update,
        returns False if its not yet time for an update
        """
        _time = time
        if _time() > self._next_update:
            self.update_data()
            self._next_update = _time() + self._interval
            return True
        return False

    def get_properties(self):
        """General properties of this node"""
        nid = self.id
        yield (b"{}/$name".format(nid), self.name)
        yield (b"{}/$type".format(nid), self.type)

        if self._properties:
            yield (b"{}/$properties".format(nid), b",".join(self._properties))

            for p in self._properties:
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

    def get_data(self):
        """Return the current values"""
        nid = self.id
        for p in self._properties:
            if p.data is not None:
                yield (b"{}/{}".format(nid, p.id), p.data, p.retained)

    def update_data(self):
        """Prepare new data. Measure nodes... """
        raise NotImplementedError("not implemented")

    def callback(self, topic, payload):
        """Gets called when self.subscribe has topics"""
        raise NotImplementedError("not implemented")

    def broadcast_callback(self, topic, payload):
        """Gets called when the broadcast topic receives a message"""
        pass

    def get_property_id_from_set_topic(self, topic):
        """Return the property id from topic as integer"""
        topic = topic.decode()
        return int(topic.split("/")[-3].split("_")[-1])
