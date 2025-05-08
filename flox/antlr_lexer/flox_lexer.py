from  __future__ import annotations

from antlr4 import InputStream
from antlr4.Token import CommonToken
from antlr_lexer.FloxToken import FloxToken
from antlr_lexer.tokens import Token, TokenKind


def lex(source: str) -> list[Token]:
    lexer = FloxToken(InputStream(source))
    tokens: list[CommonToken] = get_tokens(lexer)
    filtered: list[Token] = [ ]


    for token in tokens:
        real_token: Token = as_token(lexer, token)
        if real_token: filtered.append(real_token)
    return filtered + [Token(TokenKind.EOF, None, None, -1)]

def read_file(path: str) -> str:
    f = open(path)
    c = f.read()
    f.close()
    return c

def get_tokens(lexer: FloxToken) -> list[CommonToken]:
    return lexer.getAllTokens()


def as_token(l: FloxToken, ct: CommonToken) -> Token:
    match ct.type:
        case l.FUN: return Token(TokenKind.FUN, ct.text, None, ct.line)
        case l.VAR: return Token(TokenKind.VAR, ct.text, None, ct.line)
        case l.IF: return Token(TokenKind.IF, ct.text, None, ct.line)
        case l.ELSE: return Token(TokenKind.ELSE, ct.text, None, ct.line)
        case l.WHILE: return Token(TokenKind.WHILE, ct.text, None, ct.line)
        #case l.FOR: return Token(TokenKind.FOR, ct.text, None, ct.line)
        case l.BREAK: return Token(TokenKind.BREAK, ct.text, None, ct.line)
        case l.CONTINUE: return Token(TokenKind.CONTINUE, ct.text, None, ct.line)
        case l.RETURN: return Token(TokenKind.RETURN, ct.text, None, ct.line)
        case l.FLOAT: return Token(TokenKind.NUMBER, ct.text, float(ct.text), ct.line)
        case l.INT: return Token(TokenKind.NUMBER, ct.text, float(ct.text), ct.line)
        case l.STR: return Token(TokenKind.STRING, ct.text, ct.text, ct.line)
        case l.TRUE: return Token(TokenKind.TRUE, ct.text, True, ct.line)
        case l.FALSE: return Token(TokenKind.FALSE, ct.text, False, ct.line)
        case l.NULL: return Token(TokenKind.NULL, ct.text, None, ct.line)
        case l.PLUS: return Token(TokenKind.PLUS, ct.text, None, ct.line)
        case l.MINUS: return Token(TokenKind.MINUS, ct.text, None, ct.line)
        case l.STAR: return Token(TokenKind.STAR, ct.text, None, ct.line)
        case l.SLASH: return Token(TokenKind.SLASH, ct.text, None, ct.line)
        case l.MODULO: return Token(TokenKind.MOD, ct.text, None, ct.line)
        case l.EQUAL: return Token(TokenKind.EQUAL, ct.text, None, ct.line)
        case l.EQUAL_EQUAL: return Token(TokenKind.EQUAL_EQUAL, ct.text, None, ct.line)
        case l.LESS: return Token(TokenKind.LESS, ct.text, None, ct.line)
        case l.LESS_EQUAL: return Token(TokenKind.LESS_EQUAL, ct.text, None, ct.line)
        case l.GREATER: return Token(TokenKind.GREATER, ct.text, None, ct.line)
        case l.GREATER_EQUAL: return Token(TokenKind.GREATER_EQUAL, ct.text, None, ct.line)
        case l.BANG: return Token(TokenKind.BANG, ct.text, None, ct.line)
        case l.BANG_EQUAL: return Token(TokenKind.BANG_EQUAL, ct.text, None, ct.line)
        # case l.AND: return Token(TokenKind.AND, ct.text, None, ct.line)
        # case l.OR: return Token(TokenKind.OR, ct.text, None, ct.line)
        case l.SEMI: return Token(TokenKind.SEMI, ct.text, None, ct.line)
        case l.LPAR: return Token(TokenKind.LPAR, ct.text, None, ct.line)
        case l.RPAR: return Token(TokenKind.RPAR, ct.text, None, ct.line)
        case l.LBRACE: return Token(TokenKind.LBRACE, ct.text, None, ct.line)
        case l.RBRACE: return Token(TokenKind.RBRACE, ct.text, None, ct.line)
        case l.DOT: return Token(TokenKind.DOT, ct.text, None, ct.line)
        case l.COMMA: return Token(TokenKind.COMMA, ct.text, None, ct.line)
        case l.SL_COMMENT: return Token(TokenKind.COMMENT, ct.text, ct.text, ct.line)
        case l.ML_COMMENT: return Token(TokenKind.COMMENT, ct.text, ct.text, ct.line)
        case l.IDENT: return Token(TokenKind.IDENT, ct.text, None, ct.line)
        case _ : return None



if __name__ == "__main__":
    tokens: list[Token] = lex(read_file("test.flox"))
    [ print(x) for x in tokens]
    # Lexer Done