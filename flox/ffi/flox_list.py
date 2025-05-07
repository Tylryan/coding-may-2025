from flox_fun import FloxCallable

class List(FloxCallable):

    def arity(self):
        return -1
    
    def call(self, eval_block, args: list[object]) -> object:
        return list(args)

class Head(FloxCallable):
    def arity(self):
        return 1
    
    def call(self, eval_block, args: list[object]) -> object:
        if len(args) == 0:
            print("[arity-missmatch] 'head' requires an "
                  "argument of type 'List'.")
            exit(1)

        xs: object = args[0]
        if isinstance(xs, list) is False:
            print("[type-error] 'head' requires an argument "
                  "of type 'List'.")
            exit(1)

        return xs[0]

class Tail(FloxCallable):
    def arity(self):
        return 1
    
    def call(self, eval_block, args: list[object]) -> object:
        if len(args) == 0:
            print("[arity-missmatch] 'tail' requires an "
                  "argument of type 'List'.")
            exit(1)

        xs: object = args[0]
        if isinstance(xs, list) is False:
            print("[type-error] 'tail' requires an argument "
                  "of type 'List'.")
            exit(1)

        return xs[1:]
