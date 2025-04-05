from dataclasses import dataclass
from enum import StrEnum, Enum, auto

class TKind(Enum):
    INT=auto(),     # \d+
    FLOAT=auto(),   # \d+\.\d+
    STR=auto(),     # "..."
    IDENT=auto(),   # [a-zA-Z_][a-zA-Z_]*
    TRUE=auto(),    # "true"
    FALSE=auto(),   # "false"
    NULL=auto(),    # "null"

    VAR=auto(),     # "var"
    FUN=auto(),     # "fun"
    RETURN=auto(),  # "return"
    PRINT=auto(),   # "print"

    IF=auto(),      # "if"
    ELSE=auto(),    # "else"
    WHILE=auto(),   # "while"
    BREAK=auto(),   # "while"


    PLUS    = auto(), # + 
    MINUS   = auto(), # -
    STAR    = auto(), # *
    SLASH   = auto(), # /
    MOD     = auto(), # %

    EQUAL         = auto(), # "="
    EQUAL_EQUAL   = auto(), # "=="
    LESS          = auto(), # "<"
    LESS_EQUAL    = auto(), # "<="
    GREATER       = auto(), # ">"
    GREATER_EQUAL = auto(), # ">="

    LPAR=auto(),   # "("
    RPAR=auto(),   # ")"
    LBRACE=auto(), # "{"
    RBRACE=auto(), # "}"
    SEMI=auto(),   # ";"
    COMMA=auto(),  # ","
    DOT=auto(),  # "."


    EOF =auto()

@dataclass
class Token:
    kind  : TKind
    lexeme: str
    value : object

# Token Helpers
def MK_INT(number: int):
    return Token(TKind.INT, str(number), number)

def MK_NULL_TOK() -> Token:
    return Token(TKind.NULL, "null", None)

def MK_STR_TOK(string: str):
    return Token(TKind.STR, str(string), string)