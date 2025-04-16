from pprint import pprint

from environment import Environment
from expr import *
from stmt import *
from tokens import Token, TokenType

class Interp:
    globals    : Environment     = Environment(None)
    environment: Environment     = globals
    locals     : dict[Expr, int] = {}

class LoxCallable:
    def arity(self) -> int:
        pass
    def call(self, interp: Interp, arguments: list[object]) -> object:
        pass


class LoxReturn(RuntimeError):
    value: object

    def __init__(self, value: object):
        self.value = value

def interpret(stmts: list[Stmt]) -> None:
    interp = Interp()

    for stmt in stmts:
        evaluate(interp, stmt)

def evaluate(interp: Interp, stmt: Stmt) -> object:
    if isinstance(stmt, Literal):
        return eval_literal(interp, stmt)
    elif isinstance(stmt, Unary):
        return eval_unary(interp, stmt)
    elif isinstance(stmt, Binary):
        return eval_binary(interp, stmt)
    elif isinstance(stmt, Grouping):
        return eval_grouping(interp, stmt)
    elif isinstance(stmt, Variable):
        return eval_variable(interp, stmt)
    elif isinstance(stmt, Assign):
        return eval_assign(interp, stmt)
    elif isinstance(stmt, Grouping):
        return eval_grouping(interp, stmt)
    elif isinstance(stmt, Logical):
        return eval_logical(interp, stmt)
    elif isinstance(stmt, Print):
        return eval_print(interp, stmt)
    elif isinstance(stmt, Block):
        return eval_block_stmt(interp, stmt)
    elif isinstance(stmt, If):
        return eval_if_stmt(interp, stmt)
    elif isinstance(stmt, While):
        return eval_while_stmt(interp, stmt)
    elif isinstance(stmt, Var):
        return eval_var_stmt(interp, stmt)
    elif isinstance(stmt, Expression):
        return eval_expr_stmt(interp, stmt)
    elif isinstance(stmt, Return):
        return eval_return_stmt(interp, stmt)
    elif isinstance(stmt, Function):
        return eval_fun_stmt(interp, stmt)
    elif isinstance(stmt, Call):
        return eval_call_expr(interp, stmt)
    
    else:
        pprint(f"[interpreter-error] unimplemented expression:`{stmt}`")
        exit(1)


def eval_call_expr(interp: Interp, expr: Call) -> object:
    callee: object = evaluate(interp, expr.callee)

    arguments: list[object] = []
    for argument in expr.arguments:
        arguments.append(evaluate(interp, argument))

    if not isinstance(callee, LoxCallable):
        print("[interpreter-error] Can only call functions.")
        exit(1)

    fun: LoxCallable = callee;
    return fun.call(interp, arguments)

def eval_fun_stmt(interp: Interp, stmt: Function) -> None:
    fun: LoxFunction = LoxFunction(stmt, 
                                   interp.environment,
                                   False)
    interp.environment.define(stmt.name.lexeme, fun)
    return None

def eval_return_stmt(interp: Interp, stmt: Return) -> None:
    value: object = None
    if stmt.value is not None:
        value = evaluate(interp, stmt.value)

    raise LoxReturn(value)

def eval_while_stmt(interp: Interp, stmt: While) -> None:
    while isTruthy(evaluate(interp, stmt.condition)):
        evaluate(interp, stmt.body)
    return None

def eval_if_stmt(interp: Interp, stmt: If) -> None:
    if isTruthy(evaluate(interp, stmt.condition)):
        evaluate(interp, stmt.thenBranch)
    elif stmt.elseBranch is not None:
        evaluate(interp, stmt.elseBranch)
    return None

def eval_block_stmt(interp: Interp, stmt: Block) -> None:
    execute_block(interp, stmt.statements, Environment(interp.environment))
    return None

def execute_block(interp: Interp, statements: list[Stmt], environment: Environment) -> None:
    previous: Environment = interp.environment

    try:
        interp.environment = environment

        for statement in statements:
            evaluate(interp, statement)
    finally:
        interp.environment = previous

def eval_var_stmt(interp: Interp, stmt: Var) -> None:
    value: object = None
    if stmt.initializer is not None:
        value = evaluate(interp, stmt.initializer)

    interp.environment.define(stmt.name.lexeme, value)
    return None

def eval_expr_stmt(interp: Interp, stmt: Expression) -> None:
    evaluate(interp, stmt.expression)
    return None

def eval_print(interp: Interp, stmt: Print) -> None:
    value: object = evaluate(interp, stmt.expression)
    print(stringify(value))
    return None

def eval_logical(interp: Interp, expr: Logical) -> object:
    left: object = evaluate(expr.left)

    if expr.operator.type == TokenType.OR:
        if isTruthy(left):
            return left
    else:
        if not isTruthy(left):
            return left

    return evaluate(interp, expr.right)

def eval_assign(interp: Interp, expr: Assign) -> object:
    value: object = evaluate(interp, expr.value)

    res = interp.environment.assign(expr.name.lexeme, value)

    if res is False:
        res = interp.globals.assign(expr.name.lexeme, value)

    if res is False:
        print(f"[interpreter-error] undefined variable: `{expr.name.lexeme}`")
        exit(1)

    return value

def eval_variable(interp: Interp, expr: Variable) -> object:
    # Try to find in the environment stack
    res = interp.environment.get(expr.name.lexeme)
    if res: return res

    # If not in current, then search globals
    return interp.globals.get(expr.name.lexeme)

def eval_grouping(interp: Interp, expr: Grouping) -> object:
    return evaluate(interp, expr.expression)

def eval_binary(interp: Interp, expr: Binary) -> object:
    left : object = evaluate(interp, expr.left)
    right: object = evaluate(interp, expr.right)

    match expr.operator.type:
        case TokenType.GREATER:
            return float(left) > float(right)
        case TokenType.GREATER_EQUAL:
            return float(left) >= float(right)
        case TokenType.LESS:
            return float(left) < float(right)
        case TokenType.LESS_EQUAL:
            return float(left) <= float(right)
        case TokenType.EQUAL_EQUAL:
            return float(left) == float(right)
        case TokenType.BANG_EQUAL:
            return float(left) != float(right)
        case TokenType.MINUS:
            return float(left) - float(right)
        case TokenType.SLASH:
            return float(left) / float(right)
        case TokenType.STAR:
            return float(left) * float(right)
        case TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        case _:
            print(f"[interpreter-error] unknown token type for binary expressions: `{expr.operator.lexeme}`")

def eval_unary(interp: Interp, expr: Unary) -> object:
    right: object = evaluate(interp, expr.expr)

    match expr.operator.type:
        case TokenType.MINUS:
            return -float(right)
        case TokenType.BANG:
            return not isTruthy(right)
        case _:
            print(f"[interpret-error] unknown unary operator: `{expr.operator.lexeme}`")
            exit(1)

def eval_literal(interp: Interp, expr: Literal) -> object:
    return expr.value


# Functions
@dataclass
class LoxFunction(LoxCallable):
    declaration  : Function
    closure      : Environment
    isInitializer: bool

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interp: Interp, arguments: list[object]) -> object:
        environment = Environment(self.closure)

        for i, param in enumerate(self.declaration.params):
            environment.define(self.declaration.params[i].lexeme,
                               arguments[i])

        try:
            execute_block(interp, 
                          self.declaration.body,
                          environment)
        except LoxReturn as rv:
            return rv.value

        return None

# ------------- Helpers
def stringify(obj: object) -> str:
    if obj is None:
        return "nil"
    if isinstance(obj, float):
        text: str = str(obj)
        if text.endswith(".0"):
            text = text[:-2]
        return text

    return str(obj)

def isEqual(a: object, b: object) -> bool:
    if a is None and b is None:
        return True
    if a is None:
        return False

    return a == b

def isTruthy(obj: object) -> bool:
    if obj is None:
        return False
    if isinstance(obj, bool):
        return obj

    return True


if __name__ == "__main__":
    from scanner import scan
    from parser import parse

    def readFile(path: str) -> str:
        f = open(path)
        c = f.read()
        f.close()
        return c
    
    source: str = readFile("tests/test-script.txt")
    tokens: list[Token] = scan(source)
    stmts: list[Stmt]   = parse(tokens)
    interpret(stmts)