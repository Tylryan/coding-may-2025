from flox_fun import FloxCallable

class PythonPrint(FloxCallable):

    def arity(self):
        return 1
    def call(self, eval_block, args: list[object]) -> object:
        [ print(x, end = "") for x in args]
        print()

