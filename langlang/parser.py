
from dataclasses import dataclass
from pprint import pprint
import sys

from lexer import lex, Token, TKind, perror
from tokens import Token, TKind, MK_INT, MK_NULL_TOK
from errors import perror

class Expr:
    pass

@dataclass
class VarDec(Expr):
    name: Token
    value: Expr

@dataclass
class Parser:
    index : int
    tokens: list[Token]
    exprs : list[Expr]

    def __init__(self, tokens: list[Token]):
        self.index  = 0
        self.tokens = tokens
        self.exprs  = []


@dataclass
class BinOp(Expr):
    left : Expr
    op   : Token
    right: Expr

@dataclass
class ConstInt(Expr):
    tok: Token

@dataclass
class Group(Expr):
    expr: Expr

@dataclass
class Null(Expr):
    token: Token

def MK_NULL_EXPR() -> Expr:
    return Null(MK_NULL_TOK())


def MK_CONST_INT(number: int):
    return ConstInt(MK_INT(number))

def CONT_INT_AS_INT(ci: ConstInt) -> int:
    return ci.tok.value

def parse(tokens: list[Token]):

    parser = Parser(tokens)

    while at_end(parser) == False:
        expr: Expr = parse_stmt_expr(parser)
        push(parser, expr)

    return parser.exprs



def parse_stmt_expr(parser: Parser) -> Expr:
    if check(parser, TKind.VAR):
        return parse_vardec(parser)
    
    return parse_expr(parser, 0)

def parse_vardec(parser):
    # Assuming we're at "var"
    assert check(parser, TKind.VAR)
    advance(parser)

    name: Token = expect(parser, TKind.IDENT, "[parser-error] expected identifier in variable declaration")

    # TODO(tyler): Eventually we'll get to assignment
    expect(parser, TKind.SEMI, "[parser-error] expected `;` after variable declaration")

    return VarDec(name, MK_NULL_EXPR())



def parse_expr(parser: Parser, min_prec: int) -> Expr:
    return parse_binop(parser, min_prec)

def parse_binop(parser: Parser, min_prec: int) -> Expr:

    left: Expr = parse_group(parser)

    while precedence(peek(parser)) >= min_prec \
        and check(parser, TKind.PLUS, TKind.MINUS, TKind.STAR):

        operator: Token = advance(parser)
        right: Expr = parse_binop(parser, precedence(peek(parser)) + 1)
        left = BinOp(left, operator, right)

    return left

def parse_group(parser: Parser) -> Expr:

    token: Token = peek(parser)

    if not check(parser, TKind.LPAR):
        return parse_int(parser)

    # LPAR is skipped with match
    advance(parser)

    # TODO(tyler): Might need to do precedence(token) + 1
    expr: Expr = parse_expr(parser, 0)
    if check(parser, TKind.RPAR) is False:
        print(peek(parser))
        perror("[parser-error] unclosed parentheses in group")

    advance(parser)

    return Group(expr)

def parse_int(parser: Parser) -> Expr:
    tok: Token = peek(parser)
    if check(parser, TKind.INT) is False:
        perror(f'[parser-error] unimplemented token: {tok}')

    advance(parser)
    return ConstInt(tok)













def precedence(tok: Token) -> int:
    assert isinstance(tok, Token)

    table = {
        TKind.PLUS: 45,
        TKind.MINUS: 45,
        TKind.STAR: 50,
        TKind.SLASH: 50,
        TKind.LPAR: 55
    }

    return table.get(tok.kind, 0)

# Checks type, but does not advance
def check(parser: Parser, *kinds: TKind) -> bool:
    tok: Token = peek(parser)

    for kind in kinds:
        if tok.kind == kind:
            return True
    return False

def matches(parser: Parser, *kinds: TKind) -> bool:
    res = check(parser, kinds)
    if res:
        advance(parser)

    return res


def advance(parser: Parser) -> Token:
    if at_end(parser):
        perror("[parser-error] parser peeked out of bounds")
    tok: Token = peek(parser)
    parser.index+=1
    return tok

def push(parser: Parser, expr: Expr) -> None:
    parser.exprs.append(expr)

def peek(parser: Parser) -> bool:
    return parser.tokens[parser.index]

def at_end(parser: Parser) -> bool:
    without_index = True if parser.index >= len(parser.tokens) \
            else False
    eof = parser.tokens[parser.index].kind == TKind.EOF
    return without_index or eof

def expect(parser: Parser, kind: TKind, err_str: str) -> Token:
    if check(parser, kind) is False:
        perror(err_str)

    return advance(parser)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("this command requires a file to run on")
        exit(1)

    file_path = sys.argv[1]

    f = open(file_path)
    c = f.read()
    f.close()

    def delim():
        return '*' * 75

    def tabs():
        return '\t' * 2

    def print_title(title):
        print(f"{delim()}\n{tabs()}{title}\n{delim()}")



    tokens: list[Token] = lex(c)

    print_title("LEXER TOKENS")
    pprint(tokens)

    print_title("BEGIN PARSING")
    pprint(parse(tokens))





