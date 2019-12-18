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
    ):
        self._data = default

        self.id = id
        self.name = name
        self.settable = settable
        self.retained = retained
        self.unit = unit
        self.datatype = datatype
        self.format = format
        self.restore = restore
        self.update = True
        self.on_message = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.update = True

    def msg_handler(self, topic, payload, retained):
        """Gets called when the property receive a message"""
        if payload_is_valid(self, payload):
            if self.on_message is None:
                self.data = payload
            else:
                self.on_message(topic, payload, retained)

            # do not re-publish the data from a retained message
            if retained:
                self.update = False
