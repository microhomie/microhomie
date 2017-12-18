""""
Reed switch door example
"""

from machine import Pin

from . import HomieNode


class Reed(HomieNode):

    def __init__(self, pin, interval=1):
        super().__init__(interval=interval)
        self.switch = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.last_status = None

    def __str__(self):
        status = 'open' if self.is_open() else 'closed'
        return 'Door is {}'.format(status)

    def is_open(self, as_str=False):
        return True if self.switch.value() else False

    def get_properties(self):
        return (
            (b'door/$type', b'door'),
            (b'door/$properties', b'open'),
            (b'door/open/$settable', b'false'),
            (b'door/open/$name', b'door'),
            (b'door/open/$datatype', b'boolean'),
            (b'door/open/$format', b'true,false')
        )

    def has_update(self):
        status = self.switch.value()
        if status != self.last_status:
            self.last_status = status
            return True
        return False

    def get_data(self):
        return ((b'door/open', self.is_open()),)
