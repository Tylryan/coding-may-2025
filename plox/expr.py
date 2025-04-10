
from tokens import Token, TokenType
from dataclasses import dataclass

class Expr:
    pass

@dataclass
class This(Expr):
    keyword: Token

@dataclass
class Super(Expr):
    keyword: Token
    method: Token


@dataclass
class Set(Expr):
    obj: Expr
    name: Token
    value: Expr


@dataclass
class Get(Expr):
    obj: Expr
    name: Token


@dataclass
class Call(Expr):
    callee: Expr
    paren    : Token
    arguments: list[Expr]

@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Assign(Expr):
    name: Token
    value: Expr

@dataclass
class Variable(Expr):
    name: Token

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Literal(Expr):
    value: object

@dataclass
class Unary(Expr):
    operator: Token
    expr: Expr