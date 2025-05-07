from flox_fun import FloxCallable

class PythonPrint(FloxCallable):

    def arity(self):
        return 1
    def call(self, eval_block, args: list[object]) -> object:
        for i, arg in enumerate(args):
            if arg is True: args[i]  = "true"
            if arg is False: args[i] = "false"
            if arg is None: args[i]  = "null"

        [ print(x, end = "") for x in args]
        print()

