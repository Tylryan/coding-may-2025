
class LRuntimeError(RuntimeError):
    token: object
    message: str

    def __init__(self, tok, message):
        self.message = message
        self.token = tok
