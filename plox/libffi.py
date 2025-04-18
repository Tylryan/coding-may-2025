
import interpreter
from lox_callable import LoxCallable



class LoxPrint(LoxCallable):

    @property
    def arity(self) -> int:
        return 1

    def call(self, interp: interpreter.Interp,
             arguments: list[object]) -> object:

        for arg in arguments:
            print(arg, end = "")
        
        print()

        return None

    def __repr__(self):
        return "<builtin fn: 'print'>"




