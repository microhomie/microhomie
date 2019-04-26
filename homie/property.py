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
        range=1,
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

        self._data = [default] * range
        self._delta = [None] * range
        self._update = True

    def __str__(self):
        return self.id

    def update_delta(self):
        self._delta = self._data.copy()

    def set_data(self, val, index=0):
        try:
            if isinstance(val, bool):
                val = str(val).lower().encode()
            self._data[index] = val
            self._update = True
        except (ValueError, IndexError):
            pass

    def get_data(self, index=0):
        return self._data[index]
