from __future__ import annotations
from dataclasses import dataclass

from tokens import Token, TokenType
from exprs import *
from stmt import *
from lox_callable import LoxCallable
from ereturn import EReturn

class Env:
    values: dict[str, object]
    enclosing: Env

    def __init__(self, enclosing: Env):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name: str, value: object) ->  None:
        self.values[name] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        print(f"[interpreter-error] Undefined variable on line {name.line}: '{name.lexeme}'")
        exit(1)

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        print(f"[interpreter-error] Undefined variable on line {name.line}: '{name.lexeme}'")
        exit(1)


@dataclass
class LoxFun(LoxCallable):
    declaration: Expr
    closure: Env

    def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
        environment: Env = Env(self.closure)

        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])

        try:
            block_eval(self.declaration.body, environment)
        except EReturn as ret_val:
            return ret_val.value

    def arity(self) -> int:
        return len(self.declaration.params)

class Interpreter:
    exprs: list[Expr]
    env: Env

global interpreter

def interpreter_init(exprs: list[Expr]) -> None:
    global interpreter
    interpreter = Interpreter()
    interpreter.exprs = exprs
    interpreter.env = Env(None)


def interpret(exprs: list[Expr]) -> object:
    interpreter_init(exprs)

    for expr in exprs:
        evaluate(expr)
        print("Next Expression")


def evaluate(expr: Expr) -> object:
    try:
        if is_lit(expr)       : return lit_eval(expr)
        elif is_binop(expr)   : return binop_eval(expr)
        elif is_grouping(expr): return grouping_eval(expr)
        elif is_variable(expr): return variable_eval(expr)
        elif is_env(expr)     : return print(interpreter.env.values)
        elif is_assign(expr)  : return assign_eval(expr)
        elif is_call(expr)    : return fun_call_eval(expr)
    except AssertionError:
        if is_expression(expr): return expression_eval(expr)
        elif is_var(expr)     : return var_eval(expr)
        elif is_block(expr)   : return block_eval(expr, Env(interpreter.env))
        elif is_function(expr): return fun_dec_eval(expr)
        elif is_return(expr)  : return return_eval(expr)
    except Exception as e:
        print(e)
        exit(1)

    print(f"[interpreter-error] unimplemented expression: `{stmt_to_str(expr)}`")
    exit(1)

def return_eval(expr: Expr) -> None:
    value: object = None
    if expr.value:
        value = evaluate(expr.value)
    raise EReturn(value)

# Callable Expr
def fun_call_eval(expr: Expr) -> object:
    callee: object = evaluate(expr.callee)

    args: list[object] = []
    for arg in expr.arguments:
        args.append(evaluate(arg))

    if isinstance(callee, LoxCallable) is False:
        print("[interpreter-error] Can only call functions")
        exit(1)

    fun: LoxCallable = callee
    return fun.call(interpreter, args)


def fun_dec_eval(fun: Expr) -> object:
    lox_fun: LoxFun = LoxFun(fun,
                             interpreter.env)
    interpreter.env.define(fun.name.lexeme, lox_fun)
    return None

def assign_eval(assign: Expr) -> object:
    value: object = evaluate(assign.value)
    interpreter.env.assign(assign.tok, value)
    return value

def variable_eval(variable: Expr) -> object:
    return interpreter.env.get(variable.tok)

def var_eval(var: Stmt) -> None:
    value: object = None

    if var.initializer != None:
        value = evaluate(var.initializer)

    interpreter.env.define(var.name.lexeme, value)
    return None

def grouping_eval(grouping: Expr) -> object:
    return evaluate(grouping.expression)

def expression_eval(expression: Stmt) -> object:
    return evaluate(expression.expression)

def block_eval(block: Stmt, env: Env) -> None:
    assert isinstance(block, Stmt)

    previous: Env = interpreter.env

    try:
        interpreter.env = env
        for stmt in block.statements:
            evaluate(stmt)
    finally:
        interpreter.env = previous
    return None

def lit_eval(expr: Expr) -> object:
    return expr.tok.literal
    

def binop_eval(expr: Expr) -> object:
    left = evaluate(expr.left)
    right = evaluate(expr.right)

    if expr.op.kind == TokenType.PLUS:
        return left + right
    elif expr.op.kind == TokenType.MINUS:
        return left - right
    elif expr.op.kind == TokenType.STAR:
        return left * right
    elif expr.op.kind == TokenType.SLASH:
        return left / right

    else:
        print(f"[interpreter-error] unimplemented binary operator: {expr.op.lexeme}")
        exit(1)



if __name__ == "__main__":
    from scanner import scan
    from parser import parse

    def read_file(path: str) -> str:
        f = open(path)
        c = f.read()
        f.close()
        return c

    tokens: list[Token] = scan(read_file("test.txt"))
    exprs: list[Expr] = parse(tokens)
    interpret(exprs)