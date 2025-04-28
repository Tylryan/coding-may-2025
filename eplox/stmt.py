from exprs import Expr, expr_to_str
from tokens import Token

class Stmt:
    kind: str = "Stmt"

def stmt_to_str(stmt: Stmt | Expr) -> str:
    try:
        return expr_to_str(stmt)
    except AssertionError:
        pass

    if is_expression(stmt):
        return expression_to_str(stmt)
    elif is_var(stmt):
        return var_to_str(stmt)
    elif is_block(stmt):
        return block_to_str(stmt)
    else:
        raise Exception(f"Unimplemented 'to_str' function for statement kind: '{stmt.kind}'")

# Expression
def expression_init(expression: Expr) -> Stmt:
    assert isinstance(expression, Expr)
    stmt = Stmt()
    stmt.kind = "Expression"
    stmt.expression = expression
    return stmt

def is_expression(stmt: object) -> bool:
    try: return stmt.kind == "Expression"
    except AttributeError: return False

def expression_to_str(expression: Stmt) -> str:
    expr = stmt_to_str(expression.expression)
    return f"Expression({expr})"

# Return
def return_init(keyword: Token, value: Expr) -> Stmt:
    assert isinstance(keyword, Token)
    assert isinstance(value, Expr)
    stmt = Stmt()
    stmt.kind = "Return"
    stmt.keyword = keyword
    stmt.value = value
    return stmt

def is_return(stmt: object) -> bool:
    try: return stmt.kind == "Return"
    except AttributeError: return False

def return_to_str(ret: Stmt) -> str:
    value: str = expr_to_str(ret.value)
    return f"Return({value})"

# Function
def function_init(name: Token, params: list[Token], body: list[Stmt]) -> Stmt:
    assert isinstance(name, Token)
    assert isinstance(params, list[Token])
    assert isinstance(body, list[Stmt])

    stmt = Stmt()
    stmt.kind = "Function"
    stmt.name =  name
    stmt.params = params
    stmt.body =  body
    return stmt

def is_function(stmt: object) -> bool:
    try: return stmt.kind == "Function"
    except AttributeError: return False

def function_to_str(ret: Stmt) -> str:
    name: str = ret.name.lexeme
    return f"Function({name})"

# While
def while_init(condition: Expr, body: Stmt) -> Stmt:
    assert isinstance(condition, Expr)
    assert isinstance(body, list[Stmt])

    stmt = Stmt()
    stmt.kind      = "While"
    stmt.condition =  condition
    stmt.body      = body
    return stmt

def is_while(stmt: object) -> bool:
    try: return stmt.kind == "While"
    except AttributeError: return False

def while_to_str(ret: Stmt) -> str:
    name: str = ret.name.lexeme
    return f"While()"

# If
def if_init(condition: Expr, thenBranch: Stmt, elseBranch: Stmt) -> Stmt:
    assert isinstance(condition, Expr)
    assert isinstance(thenBranch, Stmt)
    assert isinstance(elseBranch, Stmt | None)

    stmt = Stmt()
    stmt.kind       = "If"
    stmt.condition  =  condition
    stmt.thenBranch = thenBranch
    stmt.elseBranch = thenBranch
    return stmt

def is_if(stmt: object) -> bool:
    try: return stmt.kind == "If"
    except AttributeError: return False

def if_to_str(ret: Stmt) -> str:
    name: str = ret.name.lexeme
    return f"If()"
# Block
def block_init(statements: list[Stmt]) -> Stmt:
    assert isinstance(statements, list)

    stmt = Stmt()
    stmt.kind       = "Block"
    stmt.statements  =  statements
    return stmt

def is_block(stmt: object) -> bool:
    try: return stmt.kind == "Block"
    except AttributeError: return False

def block_to_str(block: Stmt) -> str:
    string = "Block("

    for s in block.statements:
        string+= stmt_to_str(s) + ", "
    string += ")"
    return string


# Var
def var_init(name: Token, initializer: Expr) -> Stmt:
    assert isinstance(name, Token)
    assert isinstance(initializer, Expr)

    stmt = Stmt()
    stmt.kind       = "Var"
    stmt.name  =  name
    stmt.initializer = initializer
    return stmt

def is_var(stmt: object) -> bool:
    try: return stmt.kind == "Var"
    except AttributeError: return False

def var_to_str(var: Stmt) -> str:
    name: str = var.name.lexeme
    init: Expr = expr_to_str(var.initializer)
    return f"Var('{name}', {init})"