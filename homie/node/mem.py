import gc

from . import HomieNode


class Mem(HomieNode):
    def __init__(self, interval=60):
        super().__init__(interval=interval)
        self.free = 0
        self.alloc = 0

    def __str__(self):
        return 'Memory: Free = {}, Alloc = {}'.format(self.free, self.alloc)

    def get_properties(self):
        return ()

    def update_data(self):
        self.free = gc.mem_free()
        self.alloc = gc.mem_alloc()

    def get_data(self):
        return (
            (b'$stats/mem/free', self.free),
            (b'$stats/mem/alloc', self.alloc)
        )
