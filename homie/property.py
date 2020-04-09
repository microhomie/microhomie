from uasyncio import get_event_loop, sleep_ms

from homie.constants import STRING
from homie.utils import payload_is_valid


class HomieNodeProperty:
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
        self._data = default
        self._retained = False

        self.id = id
        self.name = name
        self.settable = settable
        self.retained = retained
        self.unit = unit
        self.datatype = datatype
        self.format = format
        self.restore = restore
        self.on_message = on_message
        self.node = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

        if not self._retained:
            self.publish()
        else:
            self._retained = False

    def publish(self):
        loop = get_event_loop()
        loop.create_task(self.node.publish(self, self.data))

    def msg_handler(self, topic, payload, retained):
        """Gets called when the property receive a message"""
        if payload_is_valid(self, payload):
            if retained:
                if not self.restore:
                    return
                self._retained = retained

            if self.on_message is None:
                self.data = payload
            else:
                self.on_message(topic, payload, retained)
