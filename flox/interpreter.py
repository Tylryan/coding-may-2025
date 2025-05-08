from __future__ import annotations


from antlr_lexer.tokens import Token, TokenKind
from exprs import *
from lox_env import Env
from flox_exceptions import FloxReturn
from flox_fun import FloxFun, FloxCallable
from ffi import *

class Interpreter:
    env: Env
    index: int
    exprs: list[Expr]

    def __init__(self, exprs: list[Expr]):
        self.env = Env(None)
        self.index = 0
        self.exprs = exprs

global interpreter
def interpret(exprs: list[Expr]) -> None:
    global interpreter
    interpreter = Interpreter(exprs)
    load_ffis(interpreter.env)

    for expr in interpreter.exprs:
        evaluate(expr)

def evaluate(expr: Expr) -> object:
    if expr is None                 : return None
    elif isinstance(expr, Literal)  : return eval_literal(expr)
    elif isinstance(expr, Binary)   : return eval_binary(expr)
    elif isinstance(expr, Grouping) : return eval_grouping(expr)
    elif isinstance(expr, VarDec)   : return eval_variable_declaration(expr)
    elif isinstance(expr, Variable) : return eval_variable(expr)
    elif isinstance(expr, Environ)  : return eval_environ(expr)
    elif isinstance(expr, Block)    : return eval_block(expr, Env(interpreter.env))
    elif isinstance(expr, Assign)   : return eval_assign(expr)
    elif isinstance(expr, If)       : return eval_if(expr)
    elif isinstance(expr, Return)   : return eval_return(expr)
    elif isinstance(expr, FunDec)   : return eval_fun_declaration(expr)
    elif isinstance(expr, FunCall)  : return eval_fun_call(expr)
    elif isinstance(expr, FloxTrue) : return True
    elif isinstance(expr, FloxFalse): return False
    elif isinstance(expr, Null)     : return None


    else:
        print(f"[interpreter-error] unimplemented expression:"
              f"\n{expr.to_dict()}")
        exit(1)


def eval_fun_call(expr: FunCall) -> object:
    callee: object = evaluate(expr.name)

    if isinstance(callee, FloxCallable) is False:
        print(f"[interpreter-error] uncallable object "
              f"'{expr.name.token.lexeme}' on line {expr.name.token.line}.")
        exit(1)

    args: list[object] = []
    for arg in expr.args:
        obj: object = evaluate(arg)
        args.append(obj)
    
    # NOTE(tyler): eval_block here is a
    # function.
    return callee.call(eval_block, args)


def eval_return(ret: Return) -> object:
    raise FloxReturn(evaluate(ret.value))

def eval_fun_declaration(fun: FunDec) -> None:
    flox_fun = FloxFun(fun, interpreter.env)
    interpreter.env.define(fun.name.token, flox_fun)
    return None

def eval_if(expr: If) -> object:
    if evaluate(expr.predicate):
        return evaluate(expr.then_branch)
    else:
        return evaluate(expr.else_branch)

def eval_assign(expr: Assign) -> object:
    val: object = evaluate(expr.value)
    interpreter.env.assign(expr.name.token, val)
    return val

def eval_block(block: Block, new_env: Env) -> object:
    assert isinstance(block, Block)
    """Blocks should return the last the object of the
    last evaluated"""
    previous = interpreter.env

    last_object = Null()
    try:
        interpreter.env = new_env
        for expr in block.exprs:
            last_object = evaluate(expr)
    finally:
        interpreter.env = previous

    return last_object

def eval_environ(env: Environ) -> object:
    global interpreter
    symbol_table = interpreter.env.symbol_table
    from pprint import pprint
    pprint(symbol_table)
    return symbol_table

def eval_variable(variable: Variable) -> object:
    global interpreter
    return interpreter.env.get(variable.token)

def eval_variable_declaration(vardec: VarDec) -> object:
    global interpreter
    # 1. Save name in interpreter world
    # 2. Map value to name
    interpreter.env.define(vardec.name.token,  evaluate(vardec.value))

def eval_literal(expr: Literal) -> object:
    return expr.token.value

def eval_grouping(expr: Grouping) -> object:
    return evaluate(expr.expr)

def eval_binary(expr: Binary) -> object:
    # TODO(tyler): Will change to Expr
    left : float = evaluate(expr.left)
    right: float = evaluate(expr.right)
    op = expr.op

    if   op.lexeme == "+": return left + right
    elif op.lexeme == "-": return left - right
    elif op.lexeme == "*": return left * right
    elif op.lexeme == "/": return left / right
    elif op.lexeme == "%": return left % right

    elif op.kind == TokenKind.EQUAL_EQUAL  : return left == right
    elif op.kind == TokenKind.LESS         : return left < right
    elif op.kind == TokenKind.LESS_EQUAL   : return left <= right
    elif op.kind == TokenKind.GREATER      : return left > right
    elif op.kind == TokenKind.GREATER_EQUAL: return left >= right
    elif op.kind == TokenKind.BANG_EQUAL   : return left != right
    else:
        print(f"[interpreter-error] unimplemented operator: '{op.lexeme}'")
        exit(1)

if __name__ == "__main__":
    from antlr_lexer.flox_lexer import lex
    #from scanner import scan
    from parser import parse
    from utils import read_file

    interpret(parse(lex(read_file("tests/main.flox"))))
