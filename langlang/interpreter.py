from lexer import *
from parser import *

from pprint import pprint

@dataclass 
class Environment:
    scope: list[dict[str, Expr]]
    
    def __init__(self):
        self.scope = [{}]

    def push(self):
        self.scope.append({})

    def pop(self) -> dict[str, Expr]:
        # Do not pop global scope
        assert len(self.scope) != 1
        return self.scope.pop()

    def define(self, var_name: str, value: Expr):
        if self.get_index(var_name) == -1:
            perror(f"[interpreter-error] cannot redeclare variable `{var_name}` in the same scope.")
        self.scope[-1][var_name] = value

    def assign(self, var_name: str, expr: Expr):
        scope_index = self.get_index(var_name)
        if scope_index > 0:
            perror(f"[interpreter-error] cannot assign value to undeclared variable: `{var_name}`")
        self.scope[scope_index][var_name] = expr

    def get(self, var_name: str) -> Expr | None:
        if self.exists(var_name) is False:
            return None
        
        index = self.get_index(var_name)
        return self.scope[index][var_name]

    def exists(self, var_name: str) -> bool:
        return True if self.get_index(var_name) <= 0 else False

    # If in index, result will be <= 0
    # if not in any scope, result will be > 0
    def get_index(self, var_name) -> int:
        i = -1
        while not var_name in self.scope[i]:
            if abs(i) >= len(self.scope):
                return 1
            i-=1

        return i





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
        if isinstance(expr, Null)    : return expr
        if isinstance(expr, Variable): return expr
        if isinstance(expr, ConstInt): return expr
        if isinstance(expr, Break)   : return expr
        else: perror(f"[interpreter-error] unimplemented expression: `{expr}`")

def eval_funcall(interp: Interpreter, expr: FunCall) -> Expr:
    # Does function exist?
    fun_name: str = expr.name.token.lexeme
    lfun: LoxFun | None = interp.environ.get(fun_name)

    if not lfun:
        perror(f"[interpreter-error] attempting to call undefined function: `{fun_name}`")

    # Does the arity match?
    dec_arity = lfun.fun.arity
    call_arity = expr.arity
    
    if call_arity > dec_arity:
        perror(f"[interpreter-error] function called with too many arguments. expected {dec_arity}, but found {call_arity} in `{fun_name}`")
    elif call_arity < dec_arity:
        perror(f"[interpreter-error] function called with too few arguments. expected {dec_arity}, but found {call_arity} in `{fun_name}`")

    for i, param in enumerate(lfun.fun.params):
        arg = interp_expr(interp, expr.args[i])
        interp.environ.define(param.lexeme, arg)


    return eval_block(interp, lfun.fun.body)


def eval_fundec(interp: Interpreter, expr: Fun) -> Expr:
    name_tok: Token = expr.name
    closure: Environment = interp.environ
    interp.environ.define(name_tok.lexeme, LoxFun(expr, closure))
    return MK_NULL_EXPR()

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
    interp.environ.push()
    last_expr: Expr = MK_NULL_EXPR()
    for e in expr.exprs:
        expression = interp_expr(interp, e)
        if isinstance(last_expr, Break):
            break
        last_expr = expression
    interp.environ.pop()

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

    scope_index = interp.environ.get_index(name)
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

    if operator.kind == TKind.PLUS:
        return MK_CONST_INT(CONT_INT_AS_INT(left) + CONT_INT_AS_INT(right))
    elif operator.kind == TKind.STAR:
        return MK_CONST_INT(CONT_INT_AS_INT(left) * CONT_INT_AS_INT(right))
    elif operator.kind == TKind.GREATER:
        return MK_BOOL_EXPR(CONT_INT_AS_INT(left) > CONT_INT_AS_INT(right))
    elif operator.kind == TKind.LESS:
        return MK_BOOL_EXPR(CONT_INT_AS_INT(left) < CONT_INT_AS_INT(right))
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
    pprint(interpret(exprs))