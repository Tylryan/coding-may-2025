from utils import read_file

from tokens import Token, TokenKind

class Scanner:
    index : int
    source: str
    line  : int

    keywords = {
        "true": lambda x: Token(TokenKind.TRUE, "true", True, x),
        "false": lambda x: Token(TokenKind.FALSE, "false", False, x),
        "null": lambda x: Token(TokenKind.NULL, "null", None, x),
        "var": lambda x: Token(TokenKind.VAR, "var", None, x),
        "fun": lambda x: Token(TokenKind.FUN, "fun", None, x),
        "if": lambda x: Token(TokenKind.IF, "if", None, x),
        "else": lambda x: Token(TokenKind.ELSE, "else", None, x),
        "while": lambda x: Token(TokenKind.WHILE, "while", None, x),
        "return": lambda x: Token(TokenKind.RETURN, "return", None, x),
        "break": lambda x: Token(TokenKind.BREAK, "break", None, x),
        "continue": lambda x: Token(TokenKind.CONTINUE, "break", None, x),
    }

    def __init__(self, source: str):
        self.index = 0
        self.source = source
        self.line = 1


scanner: Scanner = None

def scan(source: str) -> list[Token]:
    global scanner
    scanner = Scanner(source)

    tokens: list[Token] = []

    while at_end() is False:
        char: str = peek()
        if char == "\n": new_line(); advance()
        elif char.isspace(): advance()
        elif char == "+": 
            tokens.append(Token(TokenKind.PLUS, advance(), None, line()))
        elif char == "-": 
            tokens.append(Token(TokenKind.MINUS, advance(), None, line()))
        elif char == "*": 
            tokens.append(Token(TokenKind.STAR, advance(), None, line()))
        elif char == "/"   : handle_slash(tokens)
        elif char == "%": tokens.append(Token(TokenKind.MOD, advance(), None, line()))

        elif char == "(": tokens.append(Token(TokenKind.LPAR, advance(), None, line()))
        elif char == ")": tokens.append(Token(TokenKind.RPAR, advance(), None, line()))
        elif char == "{": tokens.append(Token(TokenKind.LBRACE, advance(), None, line()))
        elif char == "}": tokens.append(Token(TokenKind.RBRACE, advance(), None, line()))
        elif char == ";": tokens.append(Token(TokenKind.SEMI, advance(), None, line()))
        elif char == ",": tokens.append(Token(TokenKind.COMMA, advance(), None, line()))
        elif char == ".": tokens.append(Token(TokenKind.DOT, advance(), None, line()))

        elif char == "=": handle_equal(tokens)
        elif char == "<": handle_less(tokens)
        elif char == ">": handle_greater(tokens)
        elif char == "!": handle_bang(tokens)
        elif char.isdigit(): handle_digit(tokens)
        elif char.isalpha(): handle_alpha(tokens)
        elif char == "\"": handle_string(tokens)
        else:
            print(f"[scanner-error] unimplemented character: '{peek()}'")
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
            print(f"[scanner-error] unterminated string starting on line {line_no}.")
            exit(1)
        if peek() == '"':
            advance()
            break

        string += advance()
    tokens.append(Token(TokenKind.STRING, f'"{string}"', string, line_no))
    return None

def handle_greater(tokens: list[Token]) -> None:
    less: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.GREATER_EQUAL, ">=", None, line()))
        advance()
        return
    tokens.append(Token(TokenKind.GREATER, less, None, line()))

def handle_bang(tokens: list[Token]) -> None:
    less: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.BANG_EQUAL, "!=", None, line()))
        advance()
        return
    tokens.append(Token(TokenKind.BANG, less, None, line()))

def handle_less(tokens: list[Token]) -> None:
    less: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.LESS_EQUAL, "<=", None, line()))
        advance()
        return
    tokens.append(Token(TokenKind.EQUAL, less, None, line()))

def handle_equal(tokens: list[Token]) -> None:
    equal: str = advance()
    if peek() == "=":
        tokens.append(Token(TokenKind.EQUAL_EQUAL, "==", None, line()))
        advance()
        return
    tokens.append(Token(TokenKind.EQUAL, equal, None, line()))
    return
    
def handle_alpha(tokens: list[Token]) -> None:
    global scanner
    # 1. Keyword
    # 2. Idenntifier
    line_no = line()
    string = advance()

    while peek().isspace() is False:
        string += advance()
        if string in scanner.keywords.keys():
            tokens.append(scanner.keywords[string](line()))
            return None
    
    tokens.append(Token(TokenKind.IDENT, string, None, line_no))
    return None
    

def handle_digit(tokens: list[Token]) -> None:
    number: str = advance()

    while peek().isdigit():
        number+= advance()

    if peek() != ".":
        tokens.append(Token(TokenKind.NUMBER, number, float(number), line()))
        return
    
    number += advance()
    while peek().isdigit():
        number+=advance()

    tokens.append(Token(TokenKind.NUMBER, number, float(number), line()))
    return

def handle_slash(tokens: list[Token]) -> None:
    global scanner

    slash: str = advance()
    line = scanner.line

    def handle_multiline_comment():
        string = slash
        while True:
            if at_end():
                print(f"[scanner-error] unterminated comma starting on line {line}")
                exit(1)

            if peek() == "\n":
                new_line()

            string+=peek()
            if advance() == "*" and advance() == "/":
                string = string[:-2]
                break
        tokens.append(Token(TokenKind.COMMENT, string, string, line))

    def handle_single_line_comment():
        comment = slash
        while peek() != "\n":
            comment += advance()

        comment+= advance()
        new_line()
        return tokens.append(Token(TokenKind.COMMENT, comment, comment, line))



    if peek() == "/": handle_single_line_comment()
    elif peek() == "*": handle_multiline_comment()
    else: tokens.append(Token(TokenKind.SLASH, slash, None, line))
    return None
    


def new_line() -> None:
    global scanner
    scanner.line+=1

def line() -> int:
    global scanner
    return scanner.line

def peek() -> str:
    global scanner
    if at_end(): return "\0"
    return scanner.source[scanner.index]

def at_end() -> bool:
    global scanner
    return scanner.index >= len(scanner.source)

def advance() -> str:
    global scanner
    char: str = scanner.source[scanner.index]
    scanner.index+=1
    return char

if __name__ == "__main__":
    tokens: list[Token] = scan(read_file("tests/00-scanner-test.txt"))
    [ print(tok) for tok in tokens]