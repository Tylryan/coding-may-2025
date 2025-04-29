from __future__ import annotations

from tokens import Token, TokenType
from exprs import *
from stmt import *


# In our case, a language is just a list of
# declarations.

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
        expr = parse_declaration()
        exprs.append(expr)

    return exprs

# ---------- STATEMENTS
def parse_declaration() -> Stmt:
    if matches(TokenType.VAR):
        return parse_var_dec()
    if matches(TokenType.FUN):
        return parse_function_dec()
    return parse_statement()

def parse_function_dec() -> Stmt:
    name: Token = consume(TokenType.IDENTIFIER, f"Expect function name in function on line {prev().line}.")
    consume(TokenType.LEFT_PAREN,
            f"Expect '(' after function name on line {name.line}.")

    params: list[Token] = []
    if not check(TokenType.RIGHT_PAREN):
        while True:
            params.append(consume(TokenType.IDENTIFIER,
                                  f"Expect parameter name in function signature on line {prev().line}."))
            if matches(TokenType.COMMA) is False:
                break
    consume(TokenType.RIGHT_PAREN, 
            f"Expect ')' after function parameters on line {peek().line}")
    consume(TokenType.LEFT_BRACE, 
            f"Missing '{{' after function signature on line {peek().line}")
    
    body: list[Stmt] = parse_block()
    return function_init(name, params, body)

def parse_var_dec() -> Stmt:
    name: Token = consume(TokenType.IDENTIFIER,
                          f"Expect variable name on line {prev().line}")
    initializer: Expr = None
    if matches(TokenType.EQUAL):
        initializer = parse_expression()

    consume(TokenType.SEMICOLON, 
            f"Expect ';' after variable declaration on line {prev().line}")
    return var_init(name, initializer)

def parse_statement() -> Stmt:
    if matches(TokenType.LEFT_BRACE):
        return block_init(parse_block())
    if matches(TokenType.RETURN):
        return parse_return()
    return parse_expr_stmt()

def parse_return() -> Stmt:
    keyword: Token = prev()
    value: Expr = None
    if not check(TokenType.SEMICOLON):
        value = parse_expression()
    consume(TokenType.SEMICOLON,
            f"Expect ';' after return value on line {keyword.line}.")
    return return_init(keyword, value)

def parse_block() -> list[Stmt]:
    statements: list[Stmt] = []
    while ((not check(TokenType.RIGHT_BRACE)) and (not is_at_end())):
        statements.append(parse_declaration())

    consume(TokenType.RIGHT_BRACE, f"Expect '}}' after block on line '{peek().line}'.")
    return statements

def parse_expr_stmt():
    expr: Expr = parse_expression()
    consume(TokenType.SEMICOLON, f"Expect ';' after expression statement on line {peek().line}")
    return expression_init(expr)

# -------------- EXPRESSIONS
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
    left: Expr = parse_unary()

    while matches(TokenType.STAR, TokenType.SLASH):
        op: Token = prev()
        right: Expr = parse_unary()
        left = binop_init(left, op, right)

    return left

def parse_unary() -> Expr:
    if matches(TokenType.BANG, TokenType.MINUS):
        op: Token = prev()
        right: Expr = parse_unary()
        return unary_init(op, right)
    return parse_call()

def parse_call() -> Expr:
    def finish_call(callee: Expr) -> Expr:
        args: list[Expr] = []
        if not check(TokenType.RIGHT_PAREN):
            while True:
                new_expr = parse_expression()
                args.append(new_expr)

                if matches(TokenType.COMMA) is False:
                    break
        paren: Token = consume(TokenType.RIGHT_PAREN,
                               "Expect ')' after arguments.")
        return call_init(callee, paren, args)

    expr: Expr = parse_primary()
    while True:
        if matches(TokenType.LEFT_PAREN):
            expr = finish_call(expr)
        else:
            break
    return expr

def parse_primary() -> Expr:
    
    if matches(TokenType.FALSE):
        return lit_init(prev())
    if matches(TokenType.TRUE):
        return lit_init(prev())
    if matches(TokenType.NIL):
        return lit_init(prev())

    # Just for temp debugging
    if matches(TokenType.ENV):
        return env_init()

    if matches(TokenType.NUMBER, TokenType.STRING):
        return lit_init(prev())

    if matches(TokenType.IDENTIFIER):
        return variable_init(prev())

    if matches(TokenType.LEFT_PAREN):
        expr: Expr = parse_expression()
        consume(TokenType.RIGHT_PAREN, f"Expect ')' after expression on line {peek().line}")
        return grouping_init(expr)


    print(f"[parser-error] unimplemented token: '{peek()}'.")
    exit(1)


def advance() -> bool:
    global parser
    tok: Token = parser.tokens[parser.index]
    parser.index+=1
    return tok

def is_at_end() -> bool:
    return parser.tokens[parser.index].kind == TokenType.EOF

def consume(type: TokenType, message: str) -> Token:
    if check(type):
        return advance()
    print(f"[parser-error] {message}")
    exit(1)

def peek() -> Token:
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
    def read_file(path: str) -> str:
        f = open(path)
        c = f.read()
        f.close()
        return c

    tokens = scan(read_file("test.txt"))
    exprs = parse(tokens)
    [ print(stmt_to_str(x)) for x in exprs ]
