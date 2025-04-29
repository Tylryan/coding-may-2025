
class EReturn(RuntimeError):
    value: object

    def __init__(self, value: object):
        self.value = value
    