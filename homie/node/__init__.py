from utime import time


class HomieNode(object):
    def __init__(self, name, interval=60):
        self.name = name
        self._node_id = None
        self.interval = interval
        self.next_update = time()

    def __repr__(self):
        return "{}(name={!r}, pin={!r}, interval={!r})".format(
            self.__class__.__name__, self.name, self.pin, self.interval
        )

    def __str__(self):
        """Return nice information about the object"""
        raise NotImplementedError("not implemented")

    @property
    def subscribe(self):
        return ()

    @property
    def node_id(self):
        if self._node_id is None:
            raise NotImplementedError("missing node id")
        return self._node_id

    @node_id.setter
    def node_id(self, val):
        self._node_id = val

    def has_update(self):
        """Depending on the interval:

        returns True if its time for an update,
        returns False if its not yet time for an update
        """
        _time = time
        if _time() > self.next_update:
            self.update_data()
            self.next_update = _time() + self.interval
            return True
        return False

    def get_properties(self):
        """General properties of this node"""
        raise NotImplementedError("not implemented")

    def get_data(self):
        """Return the current values"""
        raise NotImplementedError("not implemented")

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
