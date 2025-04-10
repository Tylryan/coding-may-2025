

from tokens import Token, TokenType
from stmt import *
from expr import *

class ParserState:
    tokens: list[Token]
    current: int

    def __init__(self):
        self.current = 0

class ParseError(RuntimeError):
    pass

def parse(tokens: list[Token]) -> list[Stmt]:
    parser = ParserState()
    parser.tokens = tokens

    statements: list[Stmt] = []
    while not isAtEnd(parser):
        statements.append(declaration(parser))

    return statements



# ----------------- PARSE NODES
def expression(parser: ParserState) -> Expr:
    return assignment(parser)

def assignment(parser: ParserState) -> Expr:
    expr: Expr = _or(parser)

    if matches(parser, TokenType.EQUAL):
        equals: Token = previous(parser)
        value: Expr = assignment(parser)

        if isinstance(expr, Variable):
            name: Token = expr.name
            return Assign(name, value)

        elif isinstance(expr, Get):
            return Set(expr.obj, expr.name, value)

        parse_error(parser, equals, "Invalid assignment target")

    return expr

def statement(parser: ParserState) -> Stmt:
    if matches(parser, TokenType.PRINT):
        return printStatement(parser)
    if matches(parser, TokenType.LEFT_BRACE):
        return Block(block(parser))
    if matches(parser, TokenType.IF):
        return ifStatement(parser)
    if matches(parser, TokenType.WHILE):
        return whileStatement(parser)
    if matches(parser, TokenType.RETURN):
        return returnStatement(parser)

    return expressionStmt(parser)

def returnStatement(parser: ParserState) -> Stmt:
    keyword: Token = previous(parser)
    value: Expr = None
    if not check(parser, TokenType.SEMICOLON):
        value = expression(parser)
    consume(parser, TokenType.SEMICOLON,
            "Expect ';' after return value")

    return Return(keyword, value)

def whileStatement(parser: ParserState) -> Stmt:
    consume(parser, TokenType.LEFT_PAREN,
            "Expect '(' after 'while'")
    condition: Expr = expression(parser)
    consume(parser, TokenType.RIGHT_PAREN,
            "Expect ')' after while condition")

    body: Stmt = statement(parser)
    return While(condition, body)

def ifStatement(parser: ParserState) -> Stmt:
    consume(parser, TokenType.LEFT_PAREN,
            "Expect '(' after 'if'")
    condition: Expr = expression(parser)
    consume(parser, TokenType.RIGHT_PAREN,
            "Expect ')' after if condition")

    thenBranch: Stmt = statement(parser)
    elseBranch: Stmt = None

    if (matches(parser, TokenType.ELSE)):
        elseBranch = statement(parser)

    return If(condition, thenBranch, elseBranch)

def block(parser: ParserState) -> list[Stmt]:
    statements: list[Stmt] = []
    while not check(parser, TokenType.RIGHT_BRACE) and not isAtEnd(parser):
        statements.append(declaration(parser))

    consume(parser, TokenType.RIGHT_BRACE,
            "Expect '}' after block.")
    return statements

def declaration(parser: ParserState) -> Stmt:
    try:
        if (matches(parser, TokenType.VAR)):
            return varDeclaration(parser)
        if (matches(parser, TokenType.FUN)):
            return fun(parser, "function")
        if (matches(parser, TokenType.CLASS)):
            return classDeclaration(parser)

        return statement(parser)

    except ParseError as e:
        synchronize(parser)
        return None

def classDeclaration(parser: ParserState) -> Stmt:
    name: Token = consume(parser, TokenType.IDENTIFIER,
                          "Expect class name.")
    superclass: Variable = None
    if matches(parser, TokenType.LESS):
        consume(parser, TokenType.IDENTIFIER,
                "Expect superclass name.")
        superclass = Variable(previous(parser))

    consume(parser, TokenType.LEFT_BRACE,
            "Expect '{' before class body")

    methods: list[Function] = []
    while not check(parser, TokenType.RIGHT_BRACE) and not isAtEnd(parser):
        methods.append(fun(parser, "method"))

def fun(parser: ParserState, kind: str) -> Function:
    name: Token = consume(parser, TokenType.IDENTIFIER,
                          f"Expect {kind} name.")
    consume(parser, TokenType.LEFT_PAREN, f"Expect '(' after {kind} name")
    parameters: list[Token] = []

    if not check(parser, TokenType.RIGHT_PAREN):
        while True:
            tok: Token = consume(parser, TokenType.IDENTIFIER, "Expect parameter name.")
            parameters.append(tok)
            
            if matches(TokenType.COMMA):
                break

    consume(parser, TokenType.RIGHT_PAREN, "Expect ')' after parameters")
    consume(parser, TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body")

    body: list[Stmt] = block(parser)
    return Function(name, parameters, body)

def varDeclaration(parser: ParserState) -> Stmt:
    name: Token = consume(parser, TokenType.IDENTIFIER, "Expect variable name")

    initializer: Expr  = None

    if matches(TokenType.EQUAL):
        initializer = expression(parser)

    consume(parser, TokenType.SEMICOLON, "Expect ';' after variable declaration")
    return Var(name, initializer)

def printStatement(parser: ParserState) -> Stmt:
    value: Expr = expression(parser)
    consume(parser, TokenType.SEMICOLON, "Expect ';' after print statement")
    return Print(value)

def expressionStmt(parser: ParserState) -> Stmt:
    expr: Expr = expression(parser)
    consume(parser, TokenType.SEMICOLON, "Expect ';' after expression.")
    return Expression(expr)

def _or(parser: ParserState) -> Expr:
    expr: Expr = _and(parser)

    while matches(parser, TokenType.OR):
        operator: Token = previous(parser)
        right: Expr= _and(parser)
        expr = Logical(expr, operator, right)

    return expr

def _and(parser: ParserState) -> Expr:
    expr: Expr = equality(parser)

    while matches(parser, TokenType.AND):
        operator: Token = previous(parser)
        right: Expr= equality(parser)
        expr = Logical(expr, operator, right)

    return expr

def equality(parser: ParserState) -> Expr:
    expr: Expr = comparison(parser)

    while matches(parser, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        operator: Token = previous(parser)
        right: Expr= comparison(parser)
        expr = Binary(expr, operator, right)
    return expr

def comparison(parser: ParserState) -> Expr:
    expr: Expr = term(parser)

    while matches(parser, TokenType.LESS, TokenType.LESS_EQUAL,
                  TokenType.GREATER, TokenType.GREATER_EQUAL):
        operator: Token = previous(parser)
        right: Expr= term(parser)
        expr = Binary(expr, operator, right)
    return expr

def term(parser: ParserState) -> Expr:
    expr: Expr = factor(parser)
    while matches(parser, TokenType.PLUS, TokenType.MINUS):
        operator: Token = previous(parser)
        right: Expr = factor(parser)
        expr = Binary(expr, operator, right)


    return expr


def factor(parser: ParserState) -> Expr:
    expr: Expr = unary(parser)
    while matches(parser, TokenType.SLASH, TokenType.STAR):
        operator: Token = previous(parser)
        right: Expr = unary(parser)
        expr = Binary(expr, operator, right)


    return expr

def unary(parser: ParserState) -> Expr:
    if (matches(parser, TokenType.BANG, TokenType.MINUS)):
        operator: Token = previous(parser)
        # By calling unary() again instead of the
        # next highest precedence, we are implementing
        # "Right Associativity"
        right: Expr = unary(parser)
        return Unary(operator, right)

    return call(parser)


def call(parser: ParserState) -> Expr:
    expr: Expr = primary(parser)
    while True:
        if matches(parser, TokenType.LEFT_PAREN):
            expr = finishCall(parser, expr)
        elif matches(parser, TokenType.DOT):
            name: Token = consume(parser, TokenType.IDENTIFIER,
                                  "Expect propery name after '.'.")
            expr = Get(expr, name)
        else:
            break

    return expr

def finishCall(parser: ParserState, callee: Expr) -> Expr:
    arguments: list[Expr] = []

    if not check(TokenType.RIGHT_PAREN):
        while True:
            arguments.append(expression(parser))
            if matches(parser, TokenType.COMMA):
                break
    paren: Token = consume(parser, TokenType.RIGHT_PAREN,
                           "Expect ')' after arguments.")

    return Call(callee, paren, arguments)


def primary(parser: ParserState) -> Expr:
    if (matches(parser, TokenType.FALSE)): return Literal(False)
    if (matches(parser, TokenType.TRUE)): return Literal(True)
    if (matches(parser, TokenType.NIL)): return Literal(None)

    if (matches(parser, TokenType.NUMBER, TokenType.STRING)): 
        return Literal(previous(parser).literal)

    if (matches(parser, TokenType.SUPER)):
        keyword: Token = previous(parser)
        consume(parser, TokenType.DOT, "Expect '.' after 'super'.")

        method: Token = consume(parser, TokenType.IDENTIFIER,
                                "Expect superclass method name")
        
        return Super(keyword, method)

    if (matches(parser, TokenType.THIS)):
        return This(previous(parser))

    if (matches(parser, TokenType.IDENTIFIER)):
        return This(previous(parser))

    if (matches(parser, TokenType.LEFT_PAREN)):
        expr: Expr = expression(parser)
        consume(parser, TokenType.RIGHT_PAREN, "Expect ')' after expression.")
        return Grouping(expr)
    
    raise parse_error(parser, peek(parser), "Expect expression.")

    

    

# ----------------- HELPERS

def consume(parser: ParserState, type: TokenType, message: str) -> Token:
    if (check(parser, type)):
        return advance(parser)

    raise parse_error(parser, peek(parser), message)

def parse_error(parser: ParserState, token: Token, message: str) -> ParseError:
    from lox import error
    error(peek(parser), message)
    return ParseError()

def synchronize(parser: ParserState) -> None:
    advance(parser)

    while not isAtEnd(parser):
        if previous(parser).type == TokenType.SEMICOLON:
            return

        match peek(parser).type:
            case TokenType.CLASS: return
            case TokenType.FOR: return
            case TokenType.FUN: return
            case TokenType.IF: return
            case TokenType.PRINT: return
            case TokenType.VAR: return
            case TokenType.WHILE: return

        advance(parser)

def matches(parser: ParserState, *types: TokenType) -> bool:
    for t in types:
        if check(parser, t):
            advance(parser)
            return True
    return False

def check(parser: ParserState, type: TokenType) -> bool:
    if isAtEnd(parser):
        return False
    return peek(parser).type == type

def advance(parser: ParserState) -> Token:
    if not isAtEnd(parser):
        parser.current+=1
    return previous(parser)

def isAtEnd(parser: ParserState) -> bool:
    return peek(parser).type == TokenType.EOF

def peek(parser: ParserState) -> Token:
    return parser.tokens[parser.current]

def previous(parser: ParserState) -> Token:
    return parser.tokens[parser.current - 1]


if __name__ == "__main__":
    from scanner import scan
    from pprint import pprint

    def readFile(path: str) -> str:
        f = open(path)
        contents = f.read()
        f.close()
        return contents

    path = "tests/test-script.txt"

    source: str = readFile(path)

    tokens: list[Token] = scan(source)
    statements: list[Stmt] = parse(tokens)

    [pprint(x) for x in statements]