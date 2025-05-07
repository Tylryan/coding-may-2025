from __future__ import annotations


from exprs import *
from lox_env import Env
from flox_exceptions import FloxReturn

class FloxCallable:
    def arity(self): 
        pass
    def call(self, 
             eval_block, 
             args: list[object]) -> object:
        pass

@dataclass
class FloxFun(FloxCallable):
    fun_dec: FunDec
    closure: Env

    def arity(self) -> int:
        return len(self.fun_dec.params)

    def call(self, eval_block, args: list[object]) -> object:
        env = Env(self.closure)

        for i, param in enumerate(self.fun_dec.params):
            env.define(param.token, args[i])

        try:
            eval_block(self.fun_dec.body, env)
        except FloxReturn as fr:
            return fr.value