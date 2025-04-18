from typing import Self
from tokens import Token

class Environment:
    values   : dict[str, object]
    enclosing: Self

    def __init__(self, enclosing: Self):
        self.values = {}
        self.enclosing = enclosing


    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def assign(self, name: Token, value: object) -> bool:
        assert isinstance(name, Token)
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] =  value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        print(f"[environment-error] undefined variable: '{name.lexeme}'")
        exit(1)


    def get(self, name: Token) -> object:
        assert isinstance(name, Token)

        if name.lexeme in self.values.keys():
            return self.values.get(name.lexeme)

        if self.enclosing is not None:
            return self.enclosing.get(name)

        print(f"[environment-error] undefined variable: `{name.lexeme}`")
        exit(1)
        
