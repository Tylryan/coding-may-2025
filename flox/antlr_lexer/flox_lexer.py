from  __future__ import annotations

from antlr4 import *
from FloxToken import FloxToken


def read_file(path: str) -> str:
    f = open(path)
    c = f.read()
    f.close()
    return c

def get_tokens(source: str) -> list[Token]:
    return FloxToken(InputStream(source)).getAllTokens()


[ print(x) for x in get_tokens(read_file("test.flox")) ]