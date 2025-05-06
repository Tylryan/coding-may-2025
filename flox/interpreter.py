from __future__ import annotations


from exprs import *

global globals
globals = {}

class Interpreter:
    index: int
    exprs: list[Expr]

def interpret(exprs: list[Expr]) -> None:

    for expr in exprs:
        thing: object = evaluate(expr)
        print(thing)

    print("ENV")
    print(globals)

def evaluate(expr: Expr) -> object:
    if isinstance(expr, Literal)   : return eval_literal(expr)
    elif isinstance(expr, Binary)  : return eval_binary(expr)
    elif isinstance(expr, Grouping): return eval_grouping(expr)
    elif isinstance(expr, VarDec)  : return eval_variable_declaration(expr)
    elif isinstance(expr, Variable): return eval_variable(expr)

    else:
        print(f"[interpreter-error] unimplemented expression:"
              f"\n{expr.to_dict()}")
        exit(1)

def eval_variable(variable: Variable) -> object:
    global globals
    return globals[variable.token.lexeme]

def eval_variable_declaration(vardec: VarDec) -> object:
    global globals
    # 1. Save name in interpreter world
    # 2. Map value to name
    globals[vardec.name.token.lexeme] = evaluate(vardec.value)

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
    else:
        print(f"[interpreter-error] unimplemented operator: '{op.lexeme}'")
        exit(1)

if __name__ == "__main__":
    from scanner import scan
    from parser import parse
    from utils import read_file

    interpret(parse(scan(read_file("tests/01-expr.flox"))))
