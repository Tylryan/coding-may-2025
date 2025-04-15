
from tokens import Token, TokenType
from lruntime_error import LRuntimeError

class Environment:
    values: dict[str, object]

    def __init__(self, enclosing = None):
        self.values = {}
        self.enclosing = enclosing


    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def assignAt(self, distance: int, 
                 name: Token,
                 value: object) -> None:
        self.ancestor(distance).values[name.lexeme] = value

    def assign(self, name: Token, value: object) -> None:
        # If the current scope contains the variable,
        # assign the value to that variable.
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return

        # Try assigning it to the parent environment
        # recursively.
        if self.enclosing:
            self.enclosing.assign(name, value)


        # If the variable was not found in any scope,
        # throw an error.
        raise LRuntimeError(f"undefined variable '{name.lexeme}'")

    def getAt(self, distance: int, name: str) -> object:
        return self.ancestor(distance).values.get(name)

    def get(self, name: Token) -> object:

        # Check the current scope/environemnt for
        # the variable.
        if name.lexeme in self.values.keys():
            return self.values.get(name.lexeme)

        # As long as the scope has  aparent,
        # recursively try to find the value in the
        # parent environments.
        if self.enclosing:
            return self.enclosing.get(name)

        raise LRuntimeError(name, f"Undefined variable '{name.lexeme}'")

        



    def ancestor(self, distance: int):
        environment = self

        for i in range(distance):
            environment = environment.enclosing

        return environment
