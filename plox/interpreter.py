
from environment import Environment
from expr import *
from stmt import *
from lreturn import LReturn
from lox_callables import LoxCallable, LoxFunction, LoxInstance, LoxClass
from lruntime_error import LRuntimeError


class InterpState:
    globals    : Environment
    environment: Environment
    locals     : dict[Expr, int]

    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}


def interpret(statements: list[Stmt]) -> None:
    interp = InterpState()

    try:
        for statement in statements:
            evaluate(interp, statement)
    except LRuntimeError as e:
        from lox import runtimeError
        runtimeError(e)


def evaluate(interp: InterpState, 
             thing: Expr | Stmt) -> object:
    assert isinstance(interp, InterpState)
    
    if isinstance(thing, Return):
        return evalReturnStmt(interp, thing)
    elif isinstance(thing, Class):
        return evalClassStmt(interp, thing)
    elif isinstance(thing, While):
        return evalWhileStmt(interp, thing)
    elif isinstance(thing, Function):
        return evalFunctionStmt(interp, thing)
    elif isinstance(thing, If):
        return evalIfStmt(interp, thing)
    elif isinstance(thing, Block):
        return evalBlockStmt(interp, 
                             thing, 
                             Environment(interp.environment))
    elif isinstance(thing, Var):
        return evalVarStmt(interp, thing)
    elif isinstance(thing, Expression):
        return evalExpressionStmt(interp, thing)
    elif isinstance(thing, Print):
        return evalPrintStmt(interp, thing)
    elif isinstance(thing, Call):
        return evalCallExpr(interp, thing)
    elif isinstance(thing, Logical):
        return evalLogicalExpr(interp, thing)
    elif isinstance(thing, Binary):
        return evalBinaryExpr(interp, thing)
    elif isinstance(thing, Assign):
        return evalAssignExpr(interp, thing)
    elif isinstance(thing, Variable):
        return evalVariableExpr(interp, thing)
    elif isinstance(thing, Get):
        return evalGetExpr(interp, thing)
    elif isinstance(thing, Set):
        return evalSetExpr(interp, thing)
    elif isinstance(thing, This):
        return evalThisExpr(interp, thing)
    elif isinstance(thing, Super):
        return evalSuperExpr(interp, thing)
    elif isinstance(thing, Literal):
        return evalLiteralExpr(interp, thing)
    elif isinstance(thing, Unary):
        return evalUnaryExpr(interp, thing)
    elif isinstance(thing, Grouping):
        return evalGroupingExpr(interp, thing)
    elif thing is None:
        return None

    raise LRuntimeError(thing,
                        "Unimplemented expression")



# OK
def evalExpressionStmt(interp: InterpState,
                       stmt: Expression) -> None:
    evaluate(interp, stmt.expression)
    return None

# OK
def evalClassStmt(interp: InterpState,
                  stmt   : Class):
    superclass: object = None
    if stmt.superclass:
        superclass = evaluate(interp, stmt.superclass)
        if not isinstance(superclass, LoxClass):
            from lruntime_error import LRuntimeError
            raise LRuntimeError(stmt.superclass.name,
                                "Superclass must be a class.")
    
    interp.environment.define(stmt.name.lexeme, None)
    if stmt.superclass:
        environment = Environment(environment)
        environment.define("super", superclass)

    methods: dict[str, LoxFunction] = {}

    for method in stmt.methods:
        fun: LoxFunction = LoxFunction(method,
                                       environment,
                                       method.name.lexeme == "init")
        methods[method.name.lexeme] = fun

    klass: LoxClass = LoxClass(stmt.name.lexeme,
                               superclass,
                               methods)
    if superclass:
        environment = environment.enclosing

    environment.assign(stmt.name, klass)
    return None

def evalSetExpr(interp: InterpState,
                expr: Set) -> object:

    obj: object = evaluate(interp, expr.obj)
    if not isinstance(obj, LoxInstance):
        raise LRuntimeError(expr.name,
                            "only instances have fields")

    value: LoxInstance = evaluate(interp, expr.value)
    obj.set(expr.name, value)

    return None


def evalGetExpr(interp: InterpState,
                expr: Get) -> object:
    obj: object = evaluate(interp,  expr.obj)

    if isinstance(obj, LoxInstance):
        return obj.get(expr.name)

    raise LRuntimeError(expr.name,
                        "Only instances have properties")

def evalVariableExpr(interp: InterpState,
                     expr: Variable) -> object:
    return lookUpVariable(expr.name, expr)

def evalAssignExpr(interp: InterpState,
                   expr: Assign) -> object:
    value: object = evaluate(interp, expr.value)

    distance: int = interp.locals.get(expr)
    if distance:
        interp.environment.assignAt(distance,
                                    expr.name,
                                    value)
    else:
        interp.globals.assign(expr.name, value)
    return value

def evalBinaryExpr(interp: InterpState,
                   expr: Binary) -> object:
    left: object = evaluate(interp, expr.left)
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

    return None
    

def evalLogicalExpr(interp: InterpState,
                    expr: Logical) -> object:

    left: object = evaluate(interp, expr.left)
    if expr.operator.type == TokenType.OR:
        if (isTruthy(left)):
            return left
    else:
        if not isTruthy(left):
            return left

    return evaluate(interp, expr.right)

def evalCallExpr(interp: InterpState,
                 expr   : Call) -> object:
    callee: object = evaluate(interp, expr.callee)

    arguments: list[object] = []
    for argument in expr.arguments:
        arguments.append(evaluate(interp, argument))

    if not isinstance(callee, LoxCallable):
        raise LRuntimeError(expr.paren,
                            "Can only call functions and classes")
    
    fun: LoxCallable = callee
    return fun.call(interp, arguments, evalBlockStmt)


def evalPrintStmt(interp: InterpState,
                  stmt: Print) -> None:
    value = evaluate(interp, stmt.expression)
    print(stringify(value))
    return None

def evalVarStmt(interp: InterpState,
                stmt: Var) -> None:
    assert isinstance(interp, InterpState)
    assert isinstance(interp.environment, Environment)

    value: object = None
    if stmt.initializer:
        value = evaluate(interp, stmt.initializer)

    interp.environment.define(stmt.name.lexeme, value)
    return None

def evalBlockStmt(interp: InterpState,
                  statements: list[Stmt],
                  environment: Environment) -> None:

    assert isinstance(interp, InterpState)
    assert isinstance(environment, Environment)
    previous: Environment = interp.environment

    try:
        interp.environment = environment

        for statement in statements:
            evaluate(interp, statement)
    finally:
        interp.environment = previous

def evalIfStmt(interp: InterpState,
               stmt: If) -> object:
    if isTruthy(evaluate(interp, stmt.condition)):
        evaluate(interp, stmt.thenBranch)
    elif stmt.elseBranch:
        evaluate(interp, stmt.elseBranch)

    return None

def evalFunctionStmt(interp: InterpState,
                     stmt: Function) -> object:

    fun: LoxFunction = LoxFunction(stmt, 
                                   interp.environment, 
                                   False)
    interp.environment.define(stmt.name.lexeme, fun)
    return None

def evalWhileStmt(interp: InterpState,
                  stmt: While):
    while isTruthy(evaluate(interp, stmt.condition)):
        evaluate(interp, stmt.body)
    return None



def evalReturnStmt(interp: InterpState,
                   stmt  : Return):
    value: object = None
    if stmt.value:
        value = evaluate(interp, stmt.value)

    raise LReturn(value)

# OK
def evalClassStmt(interp: InterpState,
                  stmt  : Class):
    superclass: object = None

    if stmt.superclass:
        superclass = evaluate(interp, stmt.superclass)
        if not isinstance(superclass, LoxClass):
            raise LRuntimeError(stmt.superclass.name,
                                "Superclass must be a class")

    interp.environment.define(stmt.name.lexeme, None)
    if stmt.superclass:
        interp.environment = Environment(interp.environment)
        interp.environment.define("super", superclass)

    methods: dict[str, LoxFunction] = {}
    for method in stmt.methods:
        fun: LoxFunction = LoxFunction(method,
                                       interp.environment,
                                       method.name.lexeme == "init")
        methods[method.name.lexeme] = fun

    klass = LoxClass(stmt.name.lexeme, 
                     superclass, 
                     methods)
    if superclass:
        interp.environment = interp.environment.enclosing

    interp.environment.assign(stmt.name, klass)
    return None


def evalThisExpr(interp: InterpState,
                  expr  : This):
    return lookUpVariable(interp, 
                          expr.keyword, 
                          expr)

def evalSuperExpr(interp: InterpState,
                  expr  : Super):

    distance: int = interp.locals.get(expr)
    superclass: LoxClass = interp.environment.getAt(distance,
                                                    "super")
    obj: LoxInstance = interp.environment.getAt(distance -1, "this")
    method: LoxFunction = superclass.findMethod(expr.method.lexeme)

    if method is None:
        raise LRuntimeError(expr.method,
                            f"Undefine property '{expr.method.lexeme}'.")
    
    return method.bind(obj)

def evalLiteralExpr(interp: InterpState,
                    expr: Literal) -> object:
    return expr.value


def evalUnaryExpr(interp: InterpState, expr: Unary) -> object:
    right = evaluate(interp, expr.right)

    match expr.operator.type:
        case TokenType.MINUS:
            return -(float(right))
        case TokenType.BANG:
            return not isTruthy(right)

    # Unreachable
    return None

def evalGroupingExpr(interp: InterpState,
                     expr: Grouping) -> object:
    return evaluate(interp, expr.expression)

# OK
def lookUpVariable(interp: InterpState, 
                   name: Token,
                   expr: Expr):
    distance: int = interp.locals.get(expr)
    if distance:
        return interp.environment.getAt(distance, 
                                        name.lexeme)
    return interp.globals.get(name)









# ---------- HELPERS
def isEqual(a: object, b: object) -> bool:
    if a is None and b is None:
        return True
    if a is None:
        return False
    return a == b

def isTruthy(obj: object) -> bool:
    if object is None:
        return False

    if isinstance(obj, bool):
        return bool(object)

    return True

def stringify(obj: object) -> str:
    if obj is None:
        return "nil"
    if isinstance(obj, float):
        text: str = str(obj)
        if text.endswith(".0"):
            text = text[:-2]
        return text

    return str(obj)


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
    statements: list[Stmt] = parse(tokens)
    interpret(statements)