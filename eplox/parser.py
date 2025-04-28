from __future__ import annotations

from tokens import Token, TokenType
from exprs import *
from stmt import *


global parser

class Parser:
    index : int
    tokens: list[Token]

def parser_init(tokens: list[Token]):
    global parser
    parser = Parser()
    parser.tokens = tokens
    parser.index = 0
    parser.len = len(tokens)


def parse(tokens: list[Token]) -> list[Expr]:
    parser_init(tokens)

    exprs = []
    while is_at_end() == False:
        expr = parse_expr_stmt()
        exprs.append(expr)

    return exprs

def parse_expr_stmt():
    expr: Expr = parse_expression()
    consume(TokenType.SEMICOLON, f"Expect ';' after expression statement on line {peek().line}")
    return expression_init(expr)

def parse_expression() -> Expr:
    return parse_assignment()

def parse_assignment() -> Expr:
    expr: Expr = parse_or()

    if matches(TokenType.EQUAL):
        equals: Token = prev()
        # Right associative
        value: Expr  = parse_assignment()

        if is_variable(expr):
            name: Token = expr.tok
            return assign_init(name, value)

        print(f"[parser-error] Invalid assignment target on line {equals.line}")
        exit(1)
    return expr

def parse_or() -> Expr:
    expr: Expr = parse_and()

    while matches(TokenType.OR):
        op: Token = prev()
        right: Expr = parse_and()
        expr = logical_init(expr, op, right)
    return expr


def parse_and() -> Expr:
    expr: Expr = parse_equality()

    while matches(TokenType.AND):
        op: Token = prev()
        right: Expr = parse_equality()
        expr = logical_init(expr, op, right)
    return expr

def parse_equality() -> Expr:
    expr: Expr= parse_comparison()

    while matches(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        op: Token = prev()
        right: Expr = parse_comparison()
        expr = binop_init(expr, op, right)

    return expr

def parse_comparison() -> Expr:
    expr: Expr = parse_term()

    while matches(TokenType.LESS, 
                  TokenType.LESS_EQUAL,
                  TokenType.GREATER,
                  TokenType.GREATER_EQUAL):
        op: Token = prev()
        right: Expr = parse_term()
        expr = binop_init(expr, op, right)

    return expr

def parse_term() -> Expr:
    left: Expr = parse_fact()

    while matches(TokenType.PLUS, TokenType.MINUS):
        op: Token = prev()
        right: Expr = parse_fact()
        left = binop_init(left, op, right)

    return left

def parse_fact() -> Expr:
    left: Expr = parse_primary()

    while matches(TokenType.STAR, TokenType.SLASH):
        op: Token = prev()
        right: Expr = parse_primary()
        left = binop_init(left, op, right)

    return left

def parse_unary() -> Expr:
    if matches(TokenType.BANG, TokenType.MINUS):
        op: Token = prev()
        right: Expr = parse_unary()
        return unary_init(op, right)

def parse_primary() -> Expr:
    
    if matches(TokenType.FALSE):
        return lit_init(prev())
    if matches(TokenType.TRUE):
        return lit_init(prev())
    if matches(TokenType.NIL):
        return lit_init(prev())

    if matches(TokenType.NUMBER, TokenType.STRING):
        return lit_init(prev())

    if matches(TokenType.IDENTIFIER):
        return variable_init(prev())

    if matches(TokenType.LEFT_PAREN):
        expr: Expr = parse_expression()
        consume(TokenType.RIGHT_PAREN, f"Expect ')' after expression on line {peek().line}")
        return grouping_init(expr)


    print(f"[parser-error] unimplemented token: '{peek()}")
    exit(1)


def advance() -> bool:
    global parser
    parser.index+=1

def is_at_end() -> bool:
    eof = parser.tokens[parser.index].kind == TokenType.EOF
    past = parser.index >= parser.len

    if past or eof:
        return True

    return False

def consume(type: TokenType, message: str) -> Token:
    if check(type):
        return advance()
    print(f"[parser-error] {message}")
    exit(1)

def peek() -> Token:
    if is_at_end() == True:
        return None
    return parser.tokens[parser.index]

def prev() -> Token:
    assert parser.index != 0
    return parser.tokens[parser.index - 1]

def check(kind: TokenType) -> bool:
    assert isinstance(kind, TokenType)
    if is_at_end():
        return False
    return peek().kind == kind

def matches(*kinds: TokenType) -> bool:
    for kind in kinds:
        if check(kind):
            advance()
            return True
    return False



if __name__ == "__main__":
    from scanner import scan
    tokens = scan("(5 + 10); 8 / 9;")
    exprs = parse(tokens)
    [ print(stmt_to_str(x)) for x in exprs ]
