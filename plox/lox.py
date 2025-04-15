import sys

from scanner import scan
from parser import parse
from stmt import *
from expr import *

class LoxState:
    hadError        = False
    hadRuntimeError = False
    # interpreter     = Interpreter()


class LRuntimeError(RuntimeError):

    def __init__(self, token, message: str):
        self.token = token
        self.message = message

    def getMessage(self):
        return self.message

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
        line = input("> ")
        if not line:
            break
        run(line)
        LoxState.hadError = False

def run(source: str) -> None:
    tokens: list[Token]    = scan(source)
    statements: list[Stmt] = parse(tokens)

    if LoxState.hadError:
        return

    # resolver: Resolver = new Resolver(interpreter)
    # resolver.resolve(statements)

    # if LoxState.hadError:
    #     return

    # interpreter.interpret(statements)

def serror(line: int, message: str) -> None:
    report(line, "", message)

def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error {where}: {message}", file = sys.stderr)
    LoxState.hadError = True


def error(token: Token, message: str) -> None:
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at {token.lexeme}", message)


def runtimeError(error: LRuntimeError):
    print(f"[line {error.token.line}] {error.message}")
    LoxState.hadRuntimeError = True