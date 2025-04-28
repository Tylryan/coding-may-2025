from __future__ import annotations
from tokens import Token


class Expr:
    kind: str = "Expr"

def call_init(callee: Expr, paren: Token, arguments: list[Expr]) -> Expr:
    assert isinstance(callee, Expr)
    assert isinstance(paren, Token)
    assert isinstance(arguments, list)

    expr           = Expr()
    expr.kind      = "Call"
    expr.callee    = callee
    expr.paren_tok = paren
    expr.arguments = arguments
    return expr

def logical_init(left: Expr, op: Token, right: Expr) -> Expr:
    assert isinstance(left, Expr)
    assert isinstance(op, Token)
    assert isinstance(right, Expr)
    expr       = Expr()
    expr.kind  = "Logical"
    expr.left  = left
    expr.op    = op
    expr.right = right
    return expr

def assign_init(name_token: Token, value: Expr) -> Expr:
    assert isinstance(name_token, Token)
    assert isinstance(value, Expr)
    expr       = Expr()
    expr.kind  = "Assign"
    expr.tok   = name_token
    expr.value = value
    return expr

def variable_init(token: Token) -> Expr:
    assert isinstance(token, Token)
    expr      = Expr()
    expr.kind = "Variable"
    expr.tok  = token
    return expr

def grouping_init(expr: Expr) -> Expr:
    assert isinstance(expr, Expr)
    expr             = Expr()
    expr.kind        = "Grouping"
    expr.expression  = expr
    return expr

def unary_init(operator: Token, right: Expr) -> Expr:
    assert isinstance(operator, Token)
    assert isinstance(right, Expr)
    unary_expr      = Expr()
    unary_expr.kind = "Unary"
    unary_expr.op    = operator
    unary_expr.right = right
    return unary_expr

def lit_init(number: Token) -> Expr:
    assert isinstance(number, Token)
    lit_expr = Expr()
    lit_expr.kind = "Literal"
    lit_expr.tok = number
    return lit_expr


def binop_init(left: Expr, op: Token, right: Expr) -> Expr:
    binop_expr = Expr()
    binop_expr.kind  = "BinOp"
    binop_expr.left  = left
    binop_expr.op    = op
    binop_expr.right = right
    return binop_expr


def is_instance(expr: Expr, kind: str) -> bool:
    assert isinstance(expr, Expr)
    assert isinstance(kind, str)

    return expr.kind == kind

# Call logical vairable assign grouping
def is_grouping(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Grouping"
    except AttributeError: return False

def is_assign(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Assign"
    except AttributeError: return False

def is_variable(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Variable"
    except AttributeError: return False

def is_logical(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Logical"
    except AttributeError: return False

def is_call(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Call"
    except AttributeError: return False

def is_grouping(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Grouping"
    except AttributeError: return False

def is_unary(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Unary"
    except AttributeError: return False

def is_binop(binop_expr: Expr) -> bool:
    assert isinstance(binop_expr, Expr)

    try: return binop_expr.kind == "BinOp"
    except AttributeError: return False

def is_lit(lit_expr: Expr) -> bool:
    assert isinstance(lit_expr, Expr)

    try: return lit_expr.kind == "Literal"
    except AttributeError: return False

def is_expr(expr: Expr) -> bool:
    assert isinstance(expr, Expr)

    try: return expr.kind == "Expr"
    except AttributeError: return False

def expr_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)

    if is_lit(expr):
        return lit_to_str(expr)
    elif is_binop(expr):
        return binop_to_str(expr)
    elif is_unary(expr):
        return unary_to_str(expr)
    elif is_grouping(expr):
        return grouping_to_str(expr)
    elif is_call(expr):
        return call_to_str(expr)
    elif is_assign(expr):
        return assign_to_str(expr)
    elif is_variable(expr):
        return variable_to_str(expr)
    elif is_logical(expr):
        return logical_to_str(expr)
    elif is_expr(expr):
        return expr_to_str(expr)

    try:
        print(f"Unimplemented expression: ", expr.kind)
    except Exception:
        print(f"[error] passed the wrong type. expected `expr`, found {type(expr)}")
        exit(1)

# Call logical assign variable
def call_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)
    callee: str = expr_to_str(expr.callee)
    return f"Call({callee})"

def assign_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)
    var: str = expr.tok.lexeme
    val: str = expr_to_str(expr.value)
    return f"Assign({var}, {val})"

def logical_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)
    left: str = expr_to_str(expr.left)
    right: str = expr_to_str(expr.right)
    op: str = expr.op.lexeme

    return f"Logical({left}, {op}, {right})"

def variable_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)
    name: str = expr.tok.lexeme
    return f"Variable({name})"

def grouping_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)
    expression: str = expr_to_str(expr.expression)
    return f"Grouping({expression})"

def unary_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)
    right: str = expr_to_str(expr.right)
    op   : str = expr.op.lexeme
    return f"Unary({op}, {right})"

def binop_to_str(binop_expr: Expr) -> str:
    assert isinstance(binop_expr, Expr)

    left: str = expr_to_str(binop_expr.left)
    right: str = expr_to_str(binop_expr.right)
    return f"BinOp({left}, {binop_expr.op}, {right})"

def lit_to_str(lit_expr: Expr) -> str:
    assert isinstance(lit_expr, Expr)

    return str(lit_expr.tok.literal)

def expr_to_str(expr: Expr) -> str:
    assert isinstance(expr, Expr)
    return "Expr()"


if __name__ == "__main__":
    from tokens import Token, TokenType

    one_tok = Token(TokenType.NUMBER, "1", 1, 1)
    two_tok = Token(TokenType.NUMBER, "2", 2, 1)
    plus_tok = Token(TokenType.PLUS, "+", None, 1)

    one = lit_init(one_tok)
    two = lit_init(two_tok)

    binop = binop_init(one, plus_tok, two)
    print(expr_to_str(binop))
