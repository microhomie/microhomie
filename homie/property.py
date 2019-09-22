from homie.constants import P_STRING


class HomieNodeProperty:
    def __init__(
        self,
        id,
        name=None,
        settable=False,
        retained=True,
        unit=None,
        datatype=P_STRING,
        format=None,
        default=None,
        restore=True,
    ):
        self.id = id
        self.name = name
        self.settable = settable
        self.retained = retained
        self.unit = unit
        self.datatype = datatype
        self.format = format
        self.range = range
        self.restore = restore

        if isinstance(default, bool):
            default = str(default).lower().encode()

        self._data = default
        self._update = True

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        try:
            if isinstance(value, bool):
                value = str(value).lower().encode()
            self._data = value
            self._update = True
        except (ValueError, IndexError):
            pass
