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
        return self._data[0]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for d in self._data:
            yield d

    def __contains__(self, i):
        if i in self._data:
            return True
        return False

    def __getitem__(self, i):
        return self._data[i]

    def __setitem__(self, k, v):
        try:
            if isinstance(v, bool):
                v = str(v).lower().encode()
            self._data[k] = v
            self._update = True
        except (ValueError, IndexError):
            pass

    @property
    def data(self):
        return self._data[0]

    @data.setter
    def data(self, value):
        self[0] = value

    def update_delta(self):
        self._delta = self._data.copy()
