
import interpreter



class LoxPrint(interpreter.LoxCallable):

    def arity(self) -> int:
        return 1

    def call(interp: interpreter.Interp,
             arguments: list[object]):

        for arg in arguments:
            print(arg, end = "")
        
        print()

        return None

    def __repr__(self):
        return "<builtin fn: 'print'>"




