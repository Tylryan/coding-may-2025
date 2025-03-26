from dataclasses import dataclass
from enum import StrEnum, Enum, auto

class TKind(Enum):
    INT=auto(),     # \d+
    STR=auto(),     # "..."
    IDENT=auto(),   # [a-zA-Z_][a-zA-Z_]*

    PLUS    = auto(), # + 
    MINUS   = auto(), # -
    STAR    = auto(), # *
    SLASH   = auto(), # /
    MOD     = auto(), # %
    EQUAL   = auto(), # =
    LESS    = auto(), # =
    GREATER = auto(), # =

    LPAR=auto(),   # (
    RPAR=auto(),   # )
    LBRACE=auto(), # {
    RBRACE=auto(), # }
    SEMI=auto(),   # ;


    EOF =auto()

@dataclass
class Token:
    kind  : TKind
    lexeme: str
    value : object

# Token Helpers
def MK_INT(number: int):
    return Token(TKind.INT, str(number), number)