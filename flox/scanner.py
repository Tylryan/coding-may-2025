from utils import read_file

from tokens import Token, TokenKind

class Scanner:
    index : int
    source: str
    line  : int

    keywords = {
        "true"    : lambda line_no: Token(TokenKind.TRUE    , "true"     , True , line_no),
        "false"   : lambda line_no: Token(TokenKind.FALSE   , "false"    , False, line_no),
        "null"    : lambda line_no: Token(TokenKind.NULL    , "null"     , None , line_no),
        "var"     : lambda line_no: Token(TokenKind.VAR     , "var"      , None , line_no),
        "fun"     : lambda line_no: Token(TokenKind.FUN     , "fun"      , None , line_no),
        "if"      : lambda line_no: Token(TokenKind.IF      , "if"       , None , line_no),
        "else"    : lambda line_no: Token(TokenKind.ELSE    , "else"     , None , line_no),
        "while"   : lambda line_no: Token(TokenKind.WHILE   , "while"    , None , line_no),
        "return"  : lambda line_no: Token(TokenKind.RETURN  , "return"   , None , line_no),
        "break"   : lambda line_no: Token(TokenKind.BREAK   , "break"    , None , line_no),
        "continue": lambda line_no: Token(TokenKind.CONTINUE, "continue" , None , line_no),
        "env"     : lambda line_no: Token(TokenKind.ENV     , "env"      , None , line_no),
    }

    def __init__(self, source: str):
        self.index  = 0
        self.source = source
        self.line   = 1


scanner: Scanner = None

def scan(source: str) -> list[Token]:
    global scanner
    scanner = Scanner(source)

    tokens: list[Token] = []

    while at_end() is False:

        char: str = peek()
        if char == "\n"    : new_line(); advance()
        elif char.isspace(): advance()
        elif char == "+"   : tokens.append(Token(TokenKind.PLUS  , advance(), None, line()))
        elif char == "-"   : tokens.append(Token(TokenKind.MINUS , advance(), None, line()))
        elif char == "*"   : tokens.append(Token(TokenKind.STAR  , advance(), None, line()))
        elif char == "%"   : tokens.append(Token(TokenKind.MOD   , advance(), None, line()))
        elif char == "("   : tokens.append(Token(TokenKind.LPAR  , advance(), None, line()))
        elif char == ")"   : tokens.append(Token(TokenKind.RPAR  , advance(), None, line()))
        elif char == "{"   : tokens.append(Token(TokenKind.LBRACE, advance(), None, line()))
        elif char == "}"   : tokens.append(Token(TokenKind.RBRACE, advance(), None, line()))
        elif char == ";"   : tokens.append(Token(TokenKind.SEMI  , advance(), None, line()))
        elif char == ","   : tokens.append(Token(TokenKind.COMMA , advance(), None, line()))
        elif char == "."   : tokens.append(Token(TokenKind.DOT   , advance(), None, line()))
        elif char == "="   : handle_equal(tokens)
        elif char == "<"   : handle_less(tokens)
        elif char == ">"   : handle_greater(tokens)
        elif char == "!"   : handle_bang(tokens)
        elif char.isdigit(): handle_digit(tokens)
        elif char.isalpha(): handle_alpha(tokens)
        elif char == "\""  : handle_string(tokens)
        elif char == "/"   : handle_slash(tokens)
        else:
            print(f"[scanner-error] unimplemented character: "
                  f"'{peek()}'")
            exit(1)

    tokens.append(Token(TokenKind.EOF, "EOF", None, line()))
    return tokens

def handle_string(tokens: list[Token]) -> None:
    global scanner
    line_no = line()
    advance()
    string = ""

    while True:
        if at_end():
            print(f"[scanner-error] unterminated string "
                  f"starting on line {line_no}.")
            exit(1)
        if peek() == '"':
            advance()
            break

        string += advance()
    tokens.append(Token(TokenKind.STRING, 
                        f'"{string}"', 
                        string, line_no))
    return None

def handle_greater(tokens: list[Token]) -> None:
    less: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.GREATER_EQUAL, 
                            ">=", None, line()))
        advance()
        return None

    tokens.append(Token(TokenKind.GREATER, 
                        less, None, line()))
    return None

def handle_bang(tokens: list[Token]) -> None:
    less: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.BANG_EQUAL, 
                            "!=", None, line()))
        advance()
        return None

    tokens.append(Token(TokenKind.BANG, 
                        less, None, line()))
    return None

def handle_less(tokens: list[Token]) -> None:
    less: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.LESS_EQUAL, 
                            "<=", None, line()))
        advance()
        return None

    tokens.append(Token(TokenKind.EQUAL, 
                        less, None, line()))
    return None

def handle_equal(tokens: list[Token]) -> None:
    equal: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.EQUAL_EQUAL, 
                            "==", None, line()))
        advance()
        return None

    tokens.append(Token(TokenKind.EQUAL, 
                        equal, None, line()))
    return None
    
def handle_alpha(tokens: list[Token]) -> None:
    global scanner
    # 1. Keyword
    # 2. Identifier
    line_no = line()
    string = advance()

    while at_end() is False and peek().isalnum():
        string += advance()
        if string in scanner.keywords.keys():
            tokens.append(scanner.keywords[string](line()))
            return None
    
    tokens.append(Token(TokenKind.IDENT, 
                        string, None, line_no))
    return None
    

def handle_digit(tokens: list[Token]) -> None:
    number: str = advance()

    while peek().isdigit():
        number+= advance()

    if peek() != ".":
        tokens.append(Token(TokenKind.NUMBER, 
                            number, float(number), line()))
        return None
    
    number += advance()
    while peek().isdigit():
        number+=advance()

    tokens.append(Token(TokenKind.NUMBER, 
                        number, float(number), line()))
    return None

def handle_slash(tokens: list[Token]) -> None:
    global scanner

    slash: str = advance()
    line = scanner.line

    def handle_multiline_comment():
        string = slash
        while True:
            if at_end():
                print(f"[scanner-error] unterminated comma "
                      f"starting on line {line}")
                exit(1)

            if peek() == "\n":
                new_line()

            string+=peek()
            if advance() == "*" and advance() == "/":
                string = string[:-2]
                break

        tokens.append(Token(TokenKind.COMMENT, 
                            string, string, line))
        return None

    def handle_single_line_comment():
        comment = slash
        while at_end() is False and peek() != "\n":
            comment+= advance()

        if at_end() is False:
            comment+= advance()
            new_line()

        tokens.append(Token(TokenKind.COMMENT, 
                                   comment, comment, line))
        return None

    if   peek() == "/": handle_single_line_comment()
    elif peek() == "*": handle_multiline_comment()
    else: tokens.append(Token(TokenKind.SLASH, 
                              slash, None, line))
    return None
    
def new_line() -> None:
    global scanner
    scanner.line+=1

def line() -> int:
    global scanner
    return scanner.line

def peek() -> str:
    global scanner
    return scanner.source[scanner.index]

def at_end() -> bool:
    global scanner
    return (scanner.index >= len(scanner.source))

def advance() -> str:
    global scanner
    char: str = scanner.source[scanner.index]
    scanner.index+=1
    return char

if __name__ == "__main__":
    #tokens: list[Token] = scan(read_file("tests/00-scanner-test.txt"))
    tokens: list[Token] = scan(read_file("tests/01-expr.flox"))
    [ print(tok) for tok in tokens]