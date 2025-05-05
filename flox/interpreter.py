from __future__ import annotations


from exprs import *

class Interpreter:
    index: int
    exprs: list[Expr]

def interpret(exprs: list[Expr]) -> None:

    for expr in exprs:
        thing: object = evaluate(expr)
        print(thing)

def evaluate(expr: Expr) -> object:
    if isinstance(expr, Literal)   : return eval_literal(expr)
    elif isinstance(expr, Binary)  : return eval_binary(expr)
    elif isinstance(expr, Grouping): return eval_grouping(expr)

    else:
        print(f"[interpreter-error] unimplemented expression:\n{expr.to_dict()}")
        exit(1)

def eval_literal(expr: Literal) -> object:
    return expr.token.value

def eval_grouping(expr: Grouping) -> object:
    return evaluate(expr.expr)

def eval_binary(expr: Binary) -> object:
    # TODO(tyler): Will change to Expr
    left: float  = evaluate(expr.left)
    right: float = evaluate(expr.right)
    op = expr.op

    if op.lexeme == "+":
        return left + right
    elif op.lexeme == "-":
        return left - right
    elif op.lexeme == "*":
        return left - right
    elif op.lexeme == "/":
        return left / right
    elif op.lexeme == "%":
        return left % right
    else:
        print(f"[interpreter-error] unimplemented operator: '{op.lexeme}'")
        exit(1)

if __name__ == "__main__":
    from scanner import scan
    from parser import parse
    from utils import read_file

    interpret(parse(scan(read_file("tests/01-expr.flox"))))
