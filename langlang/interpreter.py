from lexer import *
from parser import *

from pprint import pprint

@dataclass 
class Environment:
    scope: dict[str, Expr]
    
    def __init__(self, parent = None):
        self.scope = {}
        # this is Environment
        self.parent = parent

    def define(self, var_name: str, value: Expr):
        self.scope[var_name] = value

    def assign(self, var_name: str, expr: Expr):
        if var_name in self.scope:
            self.scope[var_name] = expr
        
        cop = self.parent
        while cop:
            if var_name in cop.scope:
                cop.scope[var_name] = expr
            cop = self.parent.parent

    def get(self, var_name: str) -> Expr | None:
        if var_name in self.scope:
            return self.scope[var_name]
        
        cop = self.parent
        while cop:
            if var_name in cop.scope:
                return cop.scope[var_name]
            cop = self.parent.parent
            
        return None

    def exists(self, var_name: str) -> bool:
        if self.get(var_name) is None:
            return False
        return True

@dataclass
class Interpreter:
    environ: Environment
    exprs: list[Expr]

    def __init__(self, exprs: list[Expr]):
        self.exprs   = exprs
        self.environ = Environment()

@dataclass
class LoxFun(Expr):
    fun: Fun
    closure: Environment

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
        if isinstance(expr, Block)   : return eval_block(interp, expr)
        if isinstance(expr, If)      : return eval_if(interp, expr)
        if isinstance(expr, While)   : return eval_while(interp, expr)
        if isinstance(expr, Fun)     : return eval_fundec(interp, expr)
        if isinstance(expr, FunCall) : return eval_funcall(interp, expr)
        if isinstance(expr, Return)  : return eval_return(interp, expr)
        if isinstance(expr, Null)    : return expr
        if isinstance(expr, Tru)     : return expr
        if isinstance(expr, Fals)    : return expr
        if isinstance(expr, Str)     : return expr
        if isinstance(expr, Variable): return expr
        if isinstance(expr, ConstInt): return expr
        if isinstance(expr, Break)   : return expr
        else: perror(f"[interpreter-error] unimplemented expression: `{expr}`")

def eval_return(interp: Interpreter, expr: Return) -> Expr:
    return expr

def eval_funcall(interp: Interpreter, expr: FunCall) -> Expr:
    pass


def eval_fundec(interp: Interpreter, expr: Fun) -> Expr:
    pass

def eval_while(interp: Interpreter, expr: While) -> Expr:
    res = MK_NULL_EXPR()
    while True:
        cond = interp_expr(interp, expr.cond)
        if is_falsy(cond):
            break
        res = eval_block(interp, expr.block)
        if isinstance(res, Break):
            break

    return res

def eval_if(interp: Interpreter, expr: If) -> Expr:
    
    cond: Expr = interp_expr(interp, expr.cond)

    res: Expr = MK_NULL_EXPR()
    if isinstance(cond, Tru):
        res = interp_expr(interp, expr.then_block)
    else:
        res = interp_expr(interp, expr.else_block)

    return res

# Returns the last evaluated expression
def eval_block(interp: Interpreter, expr: Block) -> Expr:
    old_env = interp.environ
    interp.environ = Environment(old_env)

    last_expr: Expr = MK_NULL_EXPR()
    for e in expr.exprs:
        expression = interp_expr(interp, e)
        if isinstance(last_expr, Break):
            break
        if isinstance(expression, Return):
            last_expr = expression
            break
        last_expr = expression

    interp.environ = old_env
    return last_expr

def eval_print(interp: Interpreter, expr: Print) -> Expr:
    value: Expr = interp_expr(interp, expr.expr)

    if isinstance(value, Variable):
        name = value.token.lexeme
        if interp.environ.exists(name) is False:
            perror(f"[interpreter-error] undefined variable in print statement: `{name}`")
        value = interp.environ.get(name)

    pprint(value)
    return value

def eval_assign(interp: Interpreter, expr: Assign) -> Expr:
    name = expr.variable.token.lexeme
    if interp.environ.exists(name) is False:
        perror(f"[interpreter-error] trying to assign value to undeclared variable: `{name}`")

    value: Expr = interp_expr(interp, expr.value)
    interp.environ.assign(name, value)

    return value

def eval_vardec(interp: Interpreter, expr: VarDec) -> Expr:
    value: Expr = interp_expr(interp, expr.value)
    interp.environ.define(expr.name.lexeme, value)

    # print("DEBUG")
    # pprint(interp)


def eval_group(interp: Interpreter, expr: Group) -> Expr:
    return interp_expr(expr.expr)

def eval_bin_op(interp: Interpreter, expr: BinOp) -> Expr:
    left : Expr = interp_expr(interp, expr.left)
    right: Expr = interp_expr(interp, expr.right)


    if isinstance(left, Variable):
        name = left.token.lexeme
        if interp.environ.exists(name) is False:
            perror(f"[interpreter-error] undefined variable: `{name}`")
        left = interp.environ.get(name)

    if isinstance(right, Variable):
        name = right.token.lexeme
        if interp.environ.exists(name) is False:
            perror(f"[interpreter-error] undefined variable: `{name}`")
        right = interp.environ.get(name)

    operator: Token = expr.op

    if isinstance(left, ConstInt):
        if operator.kind == TKind.PLUS:
            return MK_CONST_INT(CONT_INT_AS_INT(left) + CONT_INT_AS_INT(right))
        if operator.kind == TKind.MINUS:
            return MK_CONST_INT(CONT_INT_AS_INT(left) - CONT_INT_AS_INT(right))
        elif operator.kind == TKind.STAR:
            return MK_CONST_INT(CONT_INT_AS_INT(left) * CONT_INT_AS_INT(right))
        elif operator.kind == TKind.GREATER:
            return MK_BOOL_EXPR(CONT_INT_AS_INT(left) > CONT_INT_AS_INT(right))
        elif operator.kind == TKind.GREATER_EQUAL:
            return MK_BOOL_EXPR(CONT_INT_AS_INT(left) >= CONT_INT_AS_INT(right))
        elif operator.kind == TKind.LESS:
            return MK_BOOL_EXPR(CONT_INT_AS_INT(left) < CONT_INT_AS_INT(right))
        elif operator.kind == TKind.LESS_EQUAL:
            return MK_BOOL_EXPR(CONT_INT_AS_INT(left) <= CONT_INT_AS_INT(right))
        elif operator.kind == TKind.EQUAL_EQUAL:
            return MK_BOOL_EXPR(CONT_INT_AS_INT(left) == CONT_INT_AS_INT(right))
        else:
            from errors import perror
            perror(f"[interpreter-error] unimplemented operator on line [TODO]: `{operator.lexeme}`")

    if isinstance(left, Str):
        if operator.kind == TKind.PLUS:
            return MK_STR_EXPR(STR_AS_STR(left) + STR_AS_STR(right))
        else:
            from errors import perror
            perror(f"[interpreter-error] unimplemented operator on line [TODO]: `{operator.lexeme}`")


def checks(classname, *exprs: Expr) -> bool: 
    for expr in exprs:
        if isinstance(expr, classname) is False:
            return False
    return True

def is_falsy(expr: Expr) -> bool:
    if isinstance(expr, ConstInt):
        return True if expr.tok.value == 0 else False
    if isinstance(expr, Fals):
        return True
    return False


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
    interpret(exprs)