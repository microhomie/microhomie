from machine import Pin

from . import HomieNode


class PIR(HomieNode):

    def __init__(self, pin=4, interval=1):
        super().__init__(interval=interval)
        self.pir = Pin(pin, Pin.IN, pull=Pin.PULL_UP)
        self.last_pir_state = 0

    def __str__(self):
        return 'Last PIR State = {}'.format(self.last_pir_state)

    def get_properties(self):
        return (
            (b'pir/$type', b'pir'),
            (b'pir/$properties', b'motion'),
            (b'pir/motion/$settable', b'false'),
            (b'pir/motion/$datatype', b'boolean'),
            (b'pir/motion/$format', b'true,false')
        )

    def has_update(self):
        new_pir_state = self.pir.value()
        if new_pir_state != self.last_pir_state:
            self.last_pir_state = new_pir_state
            return True
        return False

    def get_data(self):
        payload = 'true' if self.last_pir_state == 1 else 'false'
        return ((b'pir/motion', payload),)
