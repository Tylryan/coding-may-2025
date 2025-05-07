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
    if matches(TokenKind.FUN):
        return parse_fun_declaration()
    return parse_expression_statement()

def parse_fun_declaration() -> Expr:
    # "fun" IDENT "(" PARAMS? ")" BodyExpr ;
    # assuming we're starting on IDENT
    name: Variable = parse_primary()

    consume(TokenKind.LPAR,
            f"missing '(' in function declaration "
            f"for '{name.token.lexeme}' on line "
            f"{peek().line}.")

    params: list[Expr] = []
    while check(TokenKind.RPAR) is False:
        if at_end():
            print(f"[parser-error] missing ')' "
                  f"in function declaration around line {name.token.lexeme}.")
            exit(1)

        if check(TokenKind.IDENT) is False:
            print(f"[parser-error] invalid parameter type in function "
                  f"declaration for '{name.token.lexeme}' "
                  f"on line {peek().line}. "
                  f"function parameters must be variable names. "
                  f"found '{peek().lexeme}'.")
            exit(1)
        param: Expr = parse_primary()
        params.append(param)

        matches(TokenKind.COMMA)

    consume(TokenKind.RPAR,
            f"missing ')' in function declaration "
            f"for '{name.token.lexeme}' on line "
            f"{peek().line}.")

    body: Expr = parse_expression()
    return FunDec(name, params, body)

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
            f"missing ';' after variable declaration "
            f"for '{name.token.lexeme}' on line "
            f"{prev().line}.")
    return vardec

def parse_expression_statement() -> Expr:
    line_start = peek().line
    if matches(TokenKind.ENV):
        return parse_env()
    


    expr: Expr = parse_expression()

    # NOTE(tyler): I'm thinking about getting rid of
    # this concept entirely and delegating the semicolon
    # check to the declarations or other expressions that
    # require them.
    # I would simply move expression_statement and just use
    # expression()
    if matches(TokenKind.SEMI): pass
    # consume(TokenKind.SEMI, 
    #         f"missing ';' after expression statement around line "
    #         f"{line_start}.")
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
    if matches(TokenKind.LBRACE):
        return parse_block()
    if matches(TokenKind.IF):
        return parse_if()
    if matches(TokenKind.RETURN):
        return parse_return()

    return parse_comparison()

def parse_if() -> Expr:
    # "if" "(" CondExpr ")" ThenExpr ("else" ElseExpr)?
    # assuming we're on Expr
    line_start: int = peek().line

    consume(TokenKind.LPAR,
            f"missing '(' in if expression around line {line_start}")
        
    predicate: Expr = parse_expression()

    consume(TokenKind.RPAR,
            f"missing ')' in if expression around line {line_start}")

    then_branch: Expr = parse_expression()

    else_branch: Expr = None
    if matches(TokenKind.ELSE):
        else_branch = parse_expression()

    return If(predicate, then_branch, else_branch)

def parse_return() -> Expr:
    # "return" Expr? ";" ;
    tok: Token = prev()
    ret_value: Expr = Null()

    if check(TokenKind.SEMI) is False:
        ret_value = parse_expression()

    consume(TokenKind.SEMI,
            f"missing ';' in return expression on line {tok.line}.")

    return Return(tok, ret_value)

def parse_comparison() -> Expr:
    left: Expr = parse_assignment()

    while matches(TokenKind.EQUAL_EQUAL,
                  TokenKind.LESS,
                  TokenKind.LESS_EQUAL,
                  TokenKind.GREATER,
                  TokenKind.GREATER_EQUAL,
                  TokenKind.BANG_EQUAL):
        op   : Token = prev()
        right: Expr = parse_assignment()
        left = Binary(left, op, right)

    return left

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
        return parse_fun_call()

    line_no = prev().line
    expr: Expr = parse_expression()
    consume(TokenKind.RPAR, f"missing ')' one line {line_no}")
    return Grouping(expr)

def parse_fun_call() -> Expr:
    # Call = IDENT ("(" Args? ")")+
    # Args = IDENT ("," IDENT)*
    name: Expr = parse_primary()
    if isinstance(name, Variable) is False:
        return name
    
    args: list[Expr]  = []
    if matches(TokenKind.LPAR):
        while True:
            if matches(TokenKind.RPAR):
                break

            expr: Expr = parse_expression()
            args.append(expr)

            if matches(TokenKind.COMMA) is False:
                break

        consume(TokenKind.RPAR,
                f"missing ')' in call for '{name.token.lexeme}' "
                f"on line {peek().line}.")

        return FunCall(name, args)
    return name



def parse_primary() -> Expr:
    if matches(TokenKind.NUMBER):
        return Literal(prev())
    if matches(TokenKind.IDENT):
        return Variable(prev())
    if matches(TokenKind.STRING):
        return Literal(prev())
    
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
    tokens: list[Token] = scan(read_file("tests/main.flox"))
    exprs: list[Expr] = parse(tokens)

    from pprint import pprint
    pprint([expr.to_dict() for expr in exprs])
    