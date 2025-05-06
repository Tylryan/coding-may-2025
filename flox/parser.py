from __future__ import annotations

from tokens import Token, TokenKind
from exprs import *
from utils import read_file

class Parser:
    index: int
    tokens: list[Token]

    def __init__(self, tokens: list[Token]):
        self.index = 0
        self.tokens = tokens

global parser
def parse(tokens: list[Token]) -> list[Expr]:
    global parser
    parser = Parser(tokens)
    exprs: list[Expr] = []

    while at_end() is False:
        expr: Expr = parse_declaration()
        if expr is None:
            continue
        exprs.append(expr)

    return exprs

def parse_declaration() -> Expr:
    if matches(TokenKind.COMMENT):
        return None
    if matches(TokenKind.VAR):
        return parse_variable_declaration()
    return parse_expression_statement()

def parse_variable_declaration() -> Expr:
    # "var" IDENT ("=" Expr)? ";"

    if check(TokenKind.IDENT) is False:
        print(f"[parser-error] missing variable identifier "
              f"in variable declaration on line {peek().line}.")
        exit(1)

    name: Variable  = parse_primary()

    value: Expr = None
    if matches(TokenKind.EQUAL):
        value = parse_expression()

    vardec = VarDec(name, value)
    consume(TokenKind.SEMI,
            f"missing ';' after variable declaration on line "
            f"{name.token.line}.")
    return vardec

def parse_expression_statement() -> Expr:
    line_start = peek().line
    if matches(TokenKind.ENV):
        return parse_env()
    if matches(TokenKind.LBRACE):
        return parse_block()


    expr: Expr = parse_expression()
    consume(TokenKind.SEMI, 
            f"missing ';' after expression statement around line "
            f"{line_start}.")
    return expr

def parse_block() -> Block:
    # Block := "{" EXPR+ "}" ;
    # assumes left brace is already matched.

    line_no = prev().line
    exprs: list[Expr] = []

    while at_end() is False and check(TokenKind.RBRACE) is False:
        expr = parse_declaration()
        exprs.append(expr)

    consume(TokenKind.RBRACE,
            f"missing '}}' in block expression on beginning on line {line_no}.")

    return Block(exprs)

# NOTE: This is really more like a statement 
def parse_env() -> Expr:
    # "env" ";"
    keyword: Token = peek()
    consume(TokenKind.SEMI,
            f"missing ';' after 'env' on line {keyword.line}.")
    return Environ(keyword)

def parse_expression() -> Expr:
    return parse_assignment()




def parse_assignment() -> Expr:
    # Assign(Variable(a), Expr)
    # a = 10;

    name: Expr = parse_term()
    if matches(TokenKind.EQUAL) is False:
        return name

    value: Expr = parse_expression()
    return Assign(name, value)


def parse_term() -> Expr:
    left: Expr = parse_fact()

    while matches(TokenKind.PLUS, TokenKind.MINUS):
        op: Token = prev()
        right: Expr = parse_fact()
        left = Binary(left, op, right)

    return left

def parse_fact() -> Expr:
    left: Expr = parse_grouping()

    while matches(TokenKind.STAR, TokenKind.SLASH, TokenKind.MOD):
        op: Token = prev()
        right: Expr = parse_grouping()
        left = Binary(left, op, right)

    return left


def parse_grouping() -> Expr:
    if matches(TokenKind.LPAR) is False:
        return parse_primary()

    line_no = prev().line
    expr: Expr = parse_expression()
    consume(TokenKind.RPAR, f"missing ')' one line {line_no}")
    return Grouping(expr)

def parse_primary() -> Expr:
    if matches(TokenKind.NUMBER):
        return Literal(prev())
    if matches(TokenKind.IDENT):
        return Variable(prev())
    
    raise Exception(f"[parser-error] unimplemented token: "
                    f"'{peek().lexeme}'")

def prev() -> Token:
    global parser
    assert parser.index > 0
    return parser.tokens[parser.index -1]

def consume(kind: TokenKind, err_msg: str) -> Token:
    if check(kind):
        return advance()
    print(f"[parser-error] {err_msg}")
    exit(1)

def matches(*kinds: TokenKind) -> bool:
    for kind in kinds:
        if check(kind):
            advance()
            return True
    return False
    
def check(kind: TokenKind) -> bool:
    return peek().kind == kind

def peek() -> Token:
    global parser
    return parser.tokens[parser.index]

def advance() -> Token:
    global parser
    tok: Token = peek()
    parser.index+=1
    return tok

def at_end() -> bool:
    global parser
    return parser.tokens[parser.index].kind == TokenKind.EOF

if __name__ == "__main__":
    from scanner import scan
    tokens: list[Token] = scan(read_file("tests/01-expr.flox"))
    exprs: list[Expr] = parse(tokens)

    from pprint import pprint
    pprint([expr.to_dict() for expr in exprs])
    