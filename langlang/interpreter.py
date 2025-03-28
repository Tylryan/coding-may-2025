from lexer import *
from parser import *

from pprint import pprint

@dataclass
class Interpreter:
    environ: dict[str, Expr]
    exprs: list[Expr]

    def __init__(self, exprs: list[Expr]):
        self.exprs   = exprs
        self.environ = {}


def interpret(exprs: list[Expr]) -> Expr:
    terp = Interpreter(exprs)

    for expr in terp.exprs:
        interp_expr(terp, expr)
    return terp

def interp_expr(interp: Interpreter, expr: Expr) -> Expr:
        if isinstance(expr, BinOp)   : return eval_bin_op(interp, expr)
        if isinstance(expr, Group)   : return eval_group(interp, expr)
        if isinstance(expr, VarDec)  : return eval_vardec(interp, expr)
        if isinstance(expr, Assign)  : return eval_assign(interp, expr)
        if isinstance(expr, Print)   : return eval_print(interp, expr)
        if isinstance(expr, Null)    : return expr
        if isinstance(expr, Variable): return expr
        if isinstance(expr, ConstInt): return expr
        else: perror(f"[interpreter-error] unimplemented expression: `{expr}`")

def eval_print(interp: Interpreter, expr: Print) -> Expr:
    value: Expr = interp_expr(interp, expr.expr)

    if isinstance(value, Variable):
        name = value.token.lexeme
        if name not in interp.environ.keys():
            perror(f"[interpreter-error] undefined variable in print statement: `{name}`")
        value = interp.environ.get(name)

    pprint(value)
    return value

def eval_assign(interp: Interpreter, expr: Assign) -> Expr:
    name = expr.variable.token.lexeme
    if name not in interp.environ:
        perror(f"[interpreter-error] trying to assign value to undeclared variable: `{name}`")

    value: Expr = interp_expr(interp, expr.value)
    interp.environ[name] = value
    print("HERE")
    pprint(interp.environ)
    return value

def eval_vardec(interp: Interpreter, expr: VarDec) -> Expr:
    value: Expr = interp_expr(interp, expr.value)
    interp.environ[expr.name.lexeme] = interp_expr(interp, value)

    # print("DEBUG")
    # pprint(interp)


def eval_group(interp: Interpreter, expr: Group) -> Expr:
    return interp_expr(expr.expr)

def eval_bin_op(interp: Interpreter, expr: BinOp) -> Expr:
    left : Expr = interp_expr(interp, expr.left)
    right: Expr = interp_expr(interp, expr.right)


    if isinstance(left, Variable):
        name = left.token.lexeme
        if name not in interp.environ.keys():
            perror(f"[interpreter-error] unefined variable: `{name}`")
        left = interp.environ.get(name)

    if isinstance(right, Variable):
        name = right.token.lexeme
        if name not in interp.environ.keys():
            perror(f"[interpreter-error] unefined variable: `{name}`")
        right = interp.environ.get(name)

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
    # pprint(exprs)
    print("OUTPUT\n")
    pprint(interpret(exprs))