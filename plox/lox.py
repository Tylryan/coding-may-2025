import sys

class LoxState:
    hadError        = False
    hadRuntimeError = False
    interpreter     = Interpreter()


def main():
    if len(sys.argv) > 1:
        print("Usage: jlox [script]")
        exit(64)

    elif len(sys.argv == 1):
        runFile(sys.argv[1])
    else:
        runPrompt()

def runFile(path: str) -> None:
    f = open(path)
    contents = f.read()
    f.close()

    run(contents)

    if LoxState.hadError:
        print(65)

    if LoxState.hadRuntimeError:
        print(70)

def runPrompt() -> None:
    while True:
        res = input("> ")
        if not res:
            break
        run(line)
        LoxState.hadError = False

def run(source: str) -> None:
    scanner                = Scanner(source)
    tokens: list[Token]    = scanner.scanTokens()
    parser: Parser         = Parser(tokens)
    statements: list[Stmt] = parser.parse()

    if LoxState.hadError:
        return

    resolver: Resolver = new Resolver(interpreter)
    resolver.resolve(statements)

    if LoxState.hadError:
        return

    interpreter.interpret(statements)


def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error {where}: {message}", file = sys.stderr)
    LoxState.hadError = True


def error(token: Token, message: str) -> None:
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at {token.lexeme}", message)


def rumtimeError(error: LRuntimeError):
    print(f"{error.getMessage()}\n[line {error.token.line}]")
    LoxState.hadRuntimeError = True