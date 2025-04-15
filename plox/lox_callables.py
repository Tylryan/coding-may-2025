
from dataclasses import dataclass
from tokens import Token
import stmt
from environment import Environment
from lreturn import LReturn

class LoxCallable:

    def arity(self):
        pass

    def call(interpreter,
             arguments: list[object]) -> object:
        pass

class LoxClass(LoxCallable):
    name      : str
    superclass: object
    methods   : dict[str, object]

    def __init__(self, name: str, 
                 superclass: object,
                 methods   : dict[str, object]):
        self.name = name
        self.superclass = superclass
        self.methods = methods


    def findMethod(self, name: str) -> object:
        if name in self.methods.keys():
            return self.methods.get(name)

        if self.superclass:
            return self.superclass.findMethod(name)

        return None

    def call(self, interp,
             eval_block_fn,
             arguments: list[object]) -> object:
        
        instance: LoxInstance = LoxInstance(self)
        initializer: LoxFunction  = self.findMethod("init")

        if initializer:
            # HERE
            initializer.bind(instance).call(interp, 
                                            arguments,
                                            eval_block_fn)

        return instance


    def arity(self):
        initializer: object = self.findMethod("init")
        if initializer is None:
            return 0

        return initializer.arity()


class LoxInstance:
    klass: LoxClass
    fields: dict[str, object]


    def __init__(self, klass: LoxClass):
        self.klass = klass
        self.fields = {}


    def set(self, name: Token, value: object) -> None:
        self.fields[name.lexeme, value]

    def get(self, name: Token) -> object:
        if name.lexeme in self.fields.keys():
            return self.fields.get(name.lexeme)

        method: LoxFunction = self.klass.findMethod(name.lexeme)
        if method:
            return method.bind(self)
        
        if method:
            return method

        from lruntime_error import LRuntimeError
        raise LRuntimeError(name,
                            f"Undefined property {name.lexeme}")

@dataclass
class LoxFunction(LoxCallable):
    declaration: stmt.Function
    closure: Environment
    isInitializer: bool


    # OK
    def bind(self, instance: LoxInstance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration,
                           environment,
                           self.isInitializer)


    def call(self, 
             interp, 
             evalBlockFn,
             arguments: list[object]) -> object:

        environment: Environment = Environment(self.closure)
        
        for i, param in enumerate(self.declaration.params):
            environment.define(self.declaration.params[i].lexeme,
                               arguments[i])

        try:
            # Execute the body of the function with the new environment
            evalBlockFn(interp, self.declaration.body, environment)
        except LReturn as returnValue:
            if self.isInitializer:
                return self.closure.getAt(0, "this")
            return returnValue.value

        if self.isInitializer:
            return self.closure.getAt(0, "this")

        return None

        
    def arity(self):
        return len(self.declaration.params)





        



