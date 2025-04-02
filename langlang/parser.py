
from dataclasses import dataclass
from pprint import pprint
import sys

from lexer import lex, Token, TKind, perror
from tokens import Token, TKind, MK_INT, MK_NULL_TOK
from errors import perror

class Expr:
    pass

@dataclass
class Print(Expr):
    expr: Expr

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
class Null(Expr):
    token: Token

@dataclass
class Tru(Expr):
    pass

@dataclass
class Fals(Expr):
    pass

@dataclass
class Variable(Expr):
    token: Token

@dataclass
class Assign(Expr):
    variable: Variable
    value: Expr

@dataclass
class Block(Expr):
    exprs: list[Expr]

@dataclass
class If(Expr):
    cond: Expr
    then_block: Block
    else_block: Block

@dataclass
class While(Expr):
    cond: Expr
    block: Block

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


def MK_NULL_EXPR() -> Expr:
    return Null(MK_NULL_TOK())

def MK_CONST_INT(number: int):
    return ConstInt(MK_INT(number))

def MK_BOOL_EXPR(boolean: bool):
    return Tru() if boolean else Fals()

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
    if check(parser, TKind.PRINT):
        return parse_print(parser)
    if check(parser, TKind.LBRACE):
        return parse_block(parser)
    
    return parse_expr(parser, 0)



    

def parse_print(parser) -> Expr:
    # Assuming we're at "print"
    advance(parser)
    expr: Expr = parse_expr(parser, 0)

    if check(parser, TKind.SEMI):
        advance(parser)

    return Print(expr)

def parse_block(parser) -> Expr:
    # Should be on "{"
    advance(parser)

    exprs: list[Expr] = []

    while not (at_end(parser) or check(parser, TKind.RBRACE)):
        expr: Expr = parse_stmt_expr(parser)
        exprs.append(expr)

    expect(parser, TKind.RBRACE, "[parser-error] missing RBRACE in block")

    return Block(exprs)

def parse_vardec(parser):
    # Assuming we're at "var"
    assert check(parser, TKind.VAR)
    advance(parser)

    name: Token = expect(parser, TKind.IDENT, "[parser-error] expected identifier in variable declaration")

    expr: Expr = MK_NULL_EXPR()
    if check(parser, TKind.SEMI):
        advance(parser)
        return VarDec(name, expr)

    # Has Expression after variable
    expect(parser, TKind.EQUAL, "[parser-error] expected `=` after variable in variable declaration")
    expr = parse_assign(parser, 0)
    # TODO(tyler): Eventually we'll get to assignment
    expect(parser, TKind.SEMI, "[parser-error] expected `;` after variable declaration")


    return VarDec(name, expr)



def parse_expr(parser: Parser, min_prec: int) -> Expr:
    return parse_assign(parser, min_prec)

def parse_assign(parser: Parser, min_prec: int) -> Expr:
    expr: Expr = parse_if(parser, min_prec)

    is_var = isinstance(expr, Variable)
    has_equal = check(parser, TKind.EQUAL)

    if not (is_var and has_equal):
        return expr

    expect(parser, TKind.EQUAL, "[parser-error] missing `=` in assignment")

    value: Expr = parse_if(parser, min_prec)

    if check(parser, TKind.SEMI):
        advance(parser)

    return Assign(expr, value)

# NOTE: Our if will be an expression
def parse_if(parser, min_prec: int) -> Expr:
    if check(parser, TKind.IF) is False:
        return parse_while(parser, min_prec)

    advance(parser) # Skip "if"

    expect(parser, TKind.LPAR, "[parser-error] missing LPAR in if expression")
    condition: Expr = parse_expr(parser, min_prec)
    expect(parser, TKind.RPAR, "[parser-error] missing RPAR in if expression")

    if check(parser, TKind.LBRACE) is False:
        perror("[parser-error] missing RBRACE in if expression")

    true_block: Block = parse_block(parser)

    else_block: Expr = MK_NULL_EXPR()

    # NOTE: This takes care of 'if else if'
    if check(parser, TKind.ELSE):
        advance(parser)
        if check(parser, TKind.IF):
            else_block = parse_if(parser, min_prec)
        else:
            else_block = parse_block(parser)

    # TODO(tyler): Replace once `else` is implemented
    return If(condition, true_block, else_block)
    
def parse_while(parser: Parser, min_prec: int) -> Expr:
    if check(parser, TKind.WHILE) is False:
        return parse_binop(parser, min_prec)

    advance(parser) # Skip "while"

    expect(parser, TKind.LPAR, "[parser-error] missing LPAR in while expression")
    condition: Expr = parse_expr(parser, min_prec)
    expect(parser, TKind.RPAR, "[parser-error] missing RPAR in while expression")

    if check(parser, TKind.LBRACE) is False:
        perror("[parser-error] missing RBRACE in while expression")

    block: Block = parse_block(parser)

    return While(condition, block)

def parse_binop(parser: Parser, min_prec: int) -> Expr:

    left: Expr = parse_group(parser)

    while precedence(peek(parser)) >= min_prec \
        and check(parser, TKind.PLUS, TKind.MINUS, TKind.STAR,
                  TKind.LESS, TKind.GREATER):

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
    expr: Expr = MK_NULL_EXPR()
    if check(parser, TKind.INT):
        expr = ConstInt(tok)
    elif check(parser, TKind.IDENT):
        expr = Variable(tok)
    else:
        perror(f"[parse-error] unimplemented token: {tok}")

    advance(parser)
    return expr













def precedence(tok: Token) -> int:
    assert isinstance(tok, Token)

    table = {
        TKind.PLUS: 45,
        TKind.MINUS: 45,
        TKind.STAR: 50,
        TKind.SLASH: 50,
        TKind.LPAR: 55,
        TKind.LESS: 40,
        TKind.GREATER: 40
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

def previous(parser: Parser) -> Token:
    if parser.index < 0:
        perror("[parser-error] previous() tried to peek out of bounds")

    return parser.tokens[parser.index]

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





