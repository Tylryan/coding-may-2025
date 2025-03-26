from lexer import *
from parser import *

class Interpreter:
    environ: dict[str, Expr]
    exprs: list[Expr]

    def __init__(self, exprs: list[Expr]):
        self.exprs   = exprs
        self.environ = {}


def interpret(exprs: list[Expr]) -> Expr:
    terp = Interpreter(exprs)

    for expr in terp.exprs:
        return interp_expr(expr)

def interp_expr(expr: Expr) -> Expr:
        if isinstance(expr, ConstInt):
            return expr
        if isinstance(expr, BinOp):
            return eval_bin_op(expr)

def eval_bin_op(expr: BinOp) -> Expr:
    left : Expr = interp_expr(expr.left)
    right: Expr = interp_expr(expr.right)

    operator: Token = expr.op

    if operator.kind == TKind.PLUS:
        return MK_CONST_INT(CONT_INT_AS_INT(left) + CONT_INT_AS_INT(right))
    elif operator.kind == TKind.STAR:
        return MK_CONST_INT(CONT_INT_AS_INT(left) * CONT_INT_AS_INT(right))
    else:
        from errors import perror
        perror(f"[interpreter-error] unimplemented operator on line [TODO]: `{operator.lexeme}`")



def checks(classname, *exprs: Expr) -> bool: 
    for expr in exprs:
        if isinstance(expr, classname) is False:
            return False
    return True


if __name__ == "__main__":
    from lexer import lex
    from parser import parse
    
    import sys
    def read_file(path: str) -> str:
        f = open(path)
        c = f.read()
        f.close()
        return c

    source: str = read_file(sys.argv[1])
    tokens: list[Token] = lex(source)
    exprs : list[Expr]  = parse(tokens)
    pprint(exprs)
    print("OUTPUT\n")
    pprint(interpret(exprs))