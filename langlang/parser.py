
from dataclasses import dataclass
from pprint import pprint
import sys

from lexer import lex, Token, TKind, perror
from tokens import Token, TKind, MK_INT, MK_NULL_TOK, MK_STR_TOK
from errors import perror

class Expr:
    pass

@dataclass
class Return(Expr):
    expr: Expr

@dataclass
class Block(Expr):
    exprs: list[Expr]

@dataclass
class Print(Expr):
    expr: Expr

@dataclass
class VarDec(Expr):
    name: Token
    value: Expr

@dataclass
class Fun(Expr):
    name  : Token
    params: list[Token]
    body  : Block
    arity : int

    def __init__(self, name, params, body):
        assert isinstance(params, list)

        self.name   = name
        self.params = params
        self.body   = body
        self.arity  = len(params)

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

    def __repr__(self):
        return "null"

@dataclass
class Tru(Expr):
    def __repr__(self):
        return "true"

@dataclass
class Fals(Expr):
    def __repr__(self):
        return "false"

@dataclass
class Str(Expr):
    tok: Token
    def __repr__(self):
        return f'"{self.tok.lexeme}"'

@dataclass
class Break(Expr):
    token: Token

@dataclass
class Variable(Expr):
    token: Token

@dataclass
class Assign(Expr):
    variable: Variable
    value: Expr


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
class FunCall(Expr):
    name : Variable
    args : list[Expr]
    arity: int

    def __init__(self, name, args):
        assert isinstance(args, list)

        self.name  = name
        self.args  = args
        self.arity = len(args)

@dataclass
class ConstInt(Expr):
    tok: Token
    def __repr__(self):
        return self.tok.lexeme

@dataclass
class Group(Expr):
    expr: Expr


def MK_NULL_EXPR() -> Expr:
    return Null(MK_NULL_TOK())

def MK_CONST_INT(number: int):
    return ConstInt(MK_INT(number))

def MK_STR_EXPR(string: str):
    return Str(MK_STR_TOK(string))

def MK_BOOL_EXPR(boolean: bool):
    return Tru() if boolean else Fals()

def CONT_INT_AS_INT(ci: ConstInt) -> int:
    return ci.tok.value

def STR_AS_STR(string: Str) -> str:
    return string.tok.value

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
    if check(parser, TKind.FUN):
        return parse_fundec(parser)
    if check(parser, TKind.LBRACE):
        return parse_block(parser)
    if check(parser, TKind.RETURN):
        return parse_return(parser)
    
    return parse_expr(parser, 0)


def parse_return(parser) -> Expr:
    # Skip "return"
    advance(parser)

    if check(parser, TKind.SEMI):
        return Return(MK_NULL_EXPR())

    res: Expr = parse_expr(parser, 0)

    if check(parser, TKind.SEMI):
        advance(parser)

    return Return(res)


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

# Currently functions will not be expressions, but statements
def parse_fundec(parser):
    # "fun" IDENT "(" PARAMS? ")" BLOCK
    # PARAMS = PARAM ("," PARAM)

    # Skip fun keyword
    advance(parser)

    name: Token = expect(parser, TKind.IDENT, 
                         "[parser-error] missing name in function declaration.")

    expect(parser, TKind.LPAR, 
           f"[parser-error] missing LPAR in function declaration: `{name.lexeme}`")
    
    params: list[Token] = []

    if check(parser, TKind.RPAR):
        # Skip RPAR
        advance(parser)
        block: Block = parse_block(parser)
        return Fun(name, params, block)

    # at this point we know the function has parameters
    while check(parser, TKind.RPAR) is False:
        if at_end(parser):
            perror(f"[parser-error] missing RPAR in function declaration: `{name.lexeme}`")

        params.append(advance(parser))

        if check(parser, TKind.COMMA):
            advance(parser)

    expect(parser, TKind.RPAR, 
           f"[parser-error] missing RPAR in function declaration: `{name.lexeme}`")
    if check(parser, TKind.LBRACE) is False:
        perror(f"[parser-error] missing LBRACE in function declaration: `{name.lexeme}`")

    block: Block = parse_block(parser)

    return Fun(name, params, block)


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

    left: Expr = parse_group(parser, min_prec)

    while precedence(peek(parser)) >= min_prec \
        and check(parser, TKind.PLUS, TKind.MINUS, TKind.STAR,
                  TKind.LESS, TKind.GREATER,
                  TKind.EQUAL_EQUAL, TKind.LESS_EQUAL, TKind.GREATER_EQUAL):

        operator: Token = advance(parser)
        right: Expr = parse_binop(parser, precedence(peek(parser)) + 1)
        left = BinOp(left, operator, right)

    return left

def parse_group(parser: Parser, min_prec: int) -> Expr:

    token: Token = peek(parser)

    if not check(parser, TKind.LPAR):
        return parse_funcall(parser, min_prec)

    # LPAR is skipped with match
    advance(parser)

    # TODO(tyler): Might need to do precedence(token) + 1
    expr: Expr = parse_expr(parser, 0)
    if check(parser, TKind.RPAR) is False:
        print(peek(parser))
        perror("[parser-error] unclosed parentheses in group")

    advance(parser)

    return Group(expr)

def parse_funcall(parser: Parser, min_prec: int) -> Expr:
    # IDENT ("(" ARGS? ")")+
    # ARGS = ARG ("," ARG)*

    expr: Expr = parse_primary(parser)

    if check(parser, TKind.LPAR) is False:
        return expr

    # Skip LPAR
    advance(parser)
    args: list[Expr] = []

    if check(parser, TKind.RPAR):
        advance(parser)
        if check(parser, TKind.SEMI):
            advance(parser)
        return FunCall(expr, args)


    while at_end(parser) is False:
        expression: Expr = parse_expr(parser, min_prec)
        args.append(expression)

        if check(parser, TKind.COMMA) is False:
            break

        advance(parser)

    expect(parser, TKind.RPAR, f"[parser-error] missing RPAR in function call: `{expr}`")

    # Just in case the function call is itself a statement expression
    if check(parser,TKind.SEMI):
        advance(parser)

    return FunCall(expr, args)




def parse_primary(parser: Parser) -> Expr:
    tok: Token = peek(parser)
    expr: Expr = MK_NULL_EXPR()
    if check(parser, TKind.INT, TKind.FLOAT):
        expr = ConstInt(tok)
    elif check(parser, TKind.IDENT):
        expr = Variable(tok)
    elif check(parser, TKind.BREAK):
        expr = Break(tok)
        # Skips "break", next advance below
        # will skip semicolon
        advance(parser)
    elif check(parser, TKind.TRUE):
        expr = Tru()
    elif check(parser, TKind.FALSE):
        expr = Fals()
    elif check(parser, TKind.STR):
        expr = Str(tok)
    elif check(parser, TKind.NULL):
        expr = Null(tok)
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
        TKind.LESS_EQUAL: 40,
        TKind.GREATER: 40,
        TKind.GREATER_EQUAL: 40,
        TKind.EQUAL_EQUAL: 40
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