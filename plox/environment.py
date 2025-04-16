from typing import Self
from tokens import Token

class Environment:
    values   : dict[str, object] = {}
    enclosing: Self

    def __init__(self, enclosing: Self):
        self.enclosing = enclosing


    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def assign(self, name: str, value: object) -> bool:
        assert isinstance(name, str)
        if name in self.values.keys():
            self.values[name] =  value
            return True

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return True

        return False


    def get(self, name: str) -> object:
        assert isinstance(name, str)
        if name in self.values.keys():
            return self.values.get(name)

        if self.enclosing is not None:
            return self.enclosing.get(name)

        print(f"[environment-error] undefined variable: `{name}`")
        exit(1)
        
