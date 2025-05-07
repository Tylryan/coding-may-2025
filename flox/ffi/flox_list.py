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


class Append(FloxCallable):
    def arity(self):
        return 2
    
    def call(self, eval_block, args: list[object]) -> object:
        if len(args) != 2:
            print("[arity-missmatch] 'append' requires two arguments (T, List).")
            exit(1)

        val: object = args[0]
        xs: object = args[1]
        if isinstance(xs, list) is False:
            print("[type-error] 'append' requires its second argument " 
                  "to be of type 'List'.")
            exit(1)

        return xs + [val]

class Prepend(FloxCallable):
    def arity(self):
        return 2
    
    def call(self, eval_block, args: list[object]) -> object:
        if len(args) != 2:
            print("[arity-missmatch] 'prepend' requires two arguments (T, List).")
            exit(1)

        val: object = args[0]
        xs: object = args[1]
        if isinstance(xs, list) is False:
            print("[type-error] 'prepend' requires its second argument " 
                  "to be of type 'List'.")
            exit(1)

        return [val] + xs

class Len(FloxCallable):
    def arity(self):
        return 1
    
    def call(self, eval_block, args: list[object]) -> object:
        if len(args) != 1:
            print("[arity-missmatch] 'len' requires one argument of type "
                  "'List'")
            exit(1)

        xs: object = args[0]
        if isinstance(xs, list) is False:
            print("[type-error] 'len' requires one argument " 
                  "of type 'List'.")
            exit(1)

        return len(xs)