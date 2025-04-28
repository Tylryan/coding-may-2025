
import pytest

from exprs import *
from tokens import *

SOME_TOKEN = Token(TokenType.AND, "", None, 0)
SOME_EXPR = Expr()

def test_call_init():
    call: Expr = call_init(SOME_EXPR, SOME_TOKEN, [SOME_EXPR])

    if is_call(call) is False:
        raise pytest.UsageError("'is_call': Expected to return True, but returned False.")

    call_to_str(call)

    expr: Expr = Expr()
    if is_call(expr):
        raise pytest.UsageError("'is_call': Expected to return False, but returned True.")

    with pytest.raises(AssertionError):
        is_call("Hello")


def test_logical_init():
    logical: Expr = logical_init(SOME_EXPR, SOME_TOKEN, SOME_EXPR)

    if is_logical(logical) is False:
        raise pytest.UsageError("'is_logical': Expected to return True, but returned False.")

    logical_to_str(logical)

    expr: Expr = Expr()
    if is_logical(expr):
        raise pytest.UsageError("'is_logical': Expected to return False, but returned True.")

    with pytest.raises(AssertionError):
        is_assign("Hello")


def test_assign_init():
    assign: Expr = assign_init(SOME_TOKEN, SOME_EXPR)

    if is_assign(assign) is False:
        raise pytest.UsageError("'is_assign': Expected to return True, but returned False.")

    assign_to_str(assign)

    expr: Expr = Expr()
    if is_assign(expr):
        raise pytest.UsageError("'is_assign': Expected to return False, but returned True.")

    with pytest.raises(AssertionError):
        is_assign("Hello")

def test_variable_init():
    variable: Expr = variable_init(SOME_TOKEN)

    if is_variable(variable) is False:
        raise pytest.UsageError("'is_variable': Expected to return True, but returned False.")

    variable_to_str(variable)

    expr: Expr = Expr()
    if is_variable(expr):
        raise pytest.UsageError("'is_variable': Expected to return False, but returned True.")

    with pytest.raises(AssertionError):
        is_variable("Hello")

#def test_grouping_init():
    #grouping: Expr = grouping_init(SOME_EXPR)

    #if is_grouping(grouping) is False:
        #raise pytest.UsageError("'is_grouping': Expected to return True, but returned False.")

    #grouping_to_str(grouping)

    #expr: Expr = Expr()
    #if is_grouping(expr):
        #raise pytest.UsageError("'is_grouping': Expected to return False, but returned True.")

    #with pytest.raises(AssertionError):
        #is_grouping("Hello")

def test_unary_init():
    unary: Expr = unary_init(SOME_TOKEN, SOME_EXPR)

    if is_unary(unary) is False:
        raise pytest.UsageError("'is_unary': Expected to return True, but returned False.")

    unary_to_str(unary)

    expr: Expr = Expr()
    if is_unary(expr):
        raise pytest.UsageError("'is_unary': Expected to return False, but returned True.")

    with pytest.raises(AssertionError):
        is_unary("Hello")

def test_binop_init():
    binop: Expr = binop_init(SOME_EXPR, SOME_TOKEN, SOME_EXPR)

    if is_binop(binop) is False:
        raise pytest.UsageError("'is_binop': Expected to return True, but returned False.")

    binop_to_str(binop)

    expr: Expr = Expr()
    if is_binop(expr):
        raise pytest.UsageError("'is_binop': Expected to return False, but returned True.")

    with pytest.raises(AssertionError):
        is_binop("Hello")

def test_lit_init():
    lit: Expr = lit_init(SOME_TOKEN)

    if is_lit(lit) is False:
        raise pytest.UsageError("'is_lit': Expected to return True, but returned False.")

    lit_to_str(lit)

    expr: Expr = Expr()
    if is_lit(expr):
        raise pytest.UsageError("'is_lit': Expected to return False, but returned True.")

    with pytest.raises(AssertionError):
        is_lit("Hello")