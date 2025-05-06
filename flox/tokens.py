from enum import Enum, auto
from dataclasses import dataclass

class TokenKind(Enum):
    # Keywords
    VAR      = auto()
    FUN      = auto()
    IF       = auto()
    WHILE    = auto()
    ELSE     = auto()
    RETURN   = auto()
    BREAK    = auto()
    CONTINUE = auto()
    ENV      = auto()

    # Types
    NUMBER = auto()
    TRUE   = auto()
    FALSE  = auto()
    NULL   = auto()
    STRING = auto()
    IDENT  = auto()

    COMMENT = auto()

    # Arithmetic Operators
    PLUS  = auto()
    MINUS = auto()
    STAR  = auto()
    SLASH = auto()
    MOD   = auto()

    # Comparison Operators
    EQUAL        = auto() # IK
    EQUAL_EQUAL  = auto()
    LESS         = auto()
    LESS_EQUAL   = auto()
    GREATER      = auto()
    GREATER_EQUAL= auto()
    BANG         = auto()
    BANG_EQUAL   = auto()

    # Punctuation
    SEMI   = auto()
    LPAR   = auto()
    RPAR   = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA  = auto()
    DOT    = auto()

    EOF = auto()


@dataclass
class Token:
    kind  : TokenKind
    lexeme: str
    value : object
    line  : int