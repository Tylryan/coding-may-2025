from dataclasses import dataclass
from enum import StrEnum, auto

class TokenType(StrEnum):
    LEFT_PAREN=auto(),
    RIGHT_PAREN=auto(), 
    LEFT_BRACE=auto(), 
    RIGHT_BRACE=auto(),
    
    COMMA=auto(), 
    DOT=auto(), 
    MINUS=auto(), 
    PLUS=auto(), 
    SEMICOLON=auto(), 
    SLASH=auto(), 
    STAR=auto(),


    BANG=auto(), 
    BANG_EQUAL=auto(), 
    EQUAL=auto(), 
    EQUAL_EQUAL=auto(),
    
    GREATER=auto(), 
    GREATER_EQUAL=auto(), 
    LESS=auto(), 
    LESS_EQUAL=auto(),


    IDENTIFIER=auto(), 
    STRING=auto(), 
    NUMBER=auto(),


    AND=auto(), 
    CLASS=auto(), 
    ELSE=auto(), 
    FALSE=auto(), 
    FUN=auto(), 
    FOR=auto(), 
    IF=auto(), 
    NIL=auto(), 
    OR=auto(),
    
    RETURN=auto(), 
    SUPER=auto(), 
    THIS=auto(), 
    TRUE=auto(), 
    VAR=auto(), 
    WHILE=auto(),
    EOF=auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int