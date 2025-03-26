
from dataclasses import dataclass
from pprint import pprint
import sys

from lexer import lex, Token, TKind, perror
from tokens import Token, TKind, MK_INT
from errors import perror

class Expr:
    pass

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

def MK_CONST_INT(number: int):
    return ConstInt(MK_INT(number))

def CONT_INT_AS_INT(ci: ConstInt) -> int:
    return ci.tok.value

def parse(tokens: list[Token]):

    parser = Parser(tokens)

    while at_end(parser) == False:
        expr: Expr = parse_expr(parser, 0)
        push(parser, expr)

    return parser.exprs

def parse_expr(parser: Parser, min_prec: int) -> Expr:
    return parse_binop(parser, min_prec)




def parse_binop(parser: Parser, min_prec: int) -> Expr:

    left: Expr = parse_int(parser)

    while precedence(peek(parser)) >= min_prec \
        and check(parser, TKind.PLUS, TKind.MINUS, TKind.STAR):

        operator: Token = advance(parser)
        right: Expr = parse_binop(parser, precedence(peek(parser)) + 1)
        left = BinOp(left, operator, right)

    return left


def parse_int(parser: Parser) -> Expr:
    tok: Token = advance(parser)
    return ConstInt(tok)













def precedence(tok: Token) -> int:
    assert isinstance(tok, Token)

    table = {
        TKind.PLUS: 45,
        TKind.MINUS: 45,
        TKind.STAR: 50,
        TKind.SLASH: 50,
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





