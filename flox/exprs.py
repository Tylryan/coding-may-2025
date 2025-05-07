from __future__ import annotations

from dataclasses import dataclass

from tokens import Token, fake_token

class Expr:

    def to_dict(self) -> dict[str, object]:
        pass

@dataclass
class Literal(Expr):
    token: Token

    def to_dict(self) -> dict[str, object]:
        return { "literal": self.token.lexeme }

@dataclass
class Binary(Expr):
    left: Expr
    op: Token
    right: Expr

    def to_dict(self) -> dict[str, object]:
        return {
            "binary-expr": {
                "left": self.left.to_dict(),
                "op"  : self.op.lexeme,
                "right": self.right.to_dict()
            }
        }

@dataclass
class Grouping(Expr):
    expr: Expr

    def to_dict(self) -> dict[str, object]:
        return { "grouping": self.expr.to_dict() }


@dataclass
class VarDec(Expr):
    name: Variable
    value: Expr

    def to_dict(self) -> dict[str, object]:
        return {
            "var-dec": {
            "name"   : self.name.to_dict(),
            "value"  : self.value.to_dict() if self.value \
                                            else "null"
            }
        }

@dataclass
class Variable(Expr):
    token: Token

    def to_dict(self) -> dict[str, object]:
        return { "variable": self.token.lexeme }

@dataclass
class Assign(Expr):
    name: Variable
    value: Expr

    def to_dict(self) -> dict[str, object]:
        return {
            "assign": {
            "name"  : self.name.to_dict() ,
            "value" : self.value.to_dict(),
            }
        }

@dataclass
class Environ(Expr):
    token: Token

    def to_dict(self) -> dict[str, object]:
        return { "env": None }

@dataclass
class Block(Expr):
    exprs: list[Expr]

    def to_dict(self) -> dict[str, object]:
        inner: list[dict[str, object]] = []
        for expr in self.exprs:
            if not expr:
                continue
            inner.append(expr.to_dict())

        return { "block": inner }

    

@dataclass
class If(Expr):
    predicate: Expr
    then_branch: Expr
    else_branch: Expr

    def to_dict(self) -> dict[str, object]:
        return {"if": {
            "predicate"  : self.predicate.to_dict(),
            "then-branch": self.then_branch.to_dict(),
            "else-branch": self.else_branch.to_dict() if self.else_branch \
                                                      else Null().to_dict()
        }}

@dataclass
class FunDec(Expr):
    name  : Variable
    params: list[Variable]
    body  : Expr


    def to_dict(self) -> dict[str, object]:
        parameters: list[dict] = []
        for param in self.params:
            parameters.append(param.to_dict())

        return {
            "function": {
                "name"  : self.name.to_dict(),
                "params": parameters,
                "body"  : self.body.to_dict()
            }
        }

@dataclass
class Return(Expr):
    token: Token
    value: Expr

    def to_dict(self) -> dict[str, object]:
        return {
            "return": {
                "value" : self.value.to_dict() if self.value else Null().to_dict()
            }
        }

@dataclass
class FunCall(Expr):
    name: Variable
    args: list[Expr]

    def to_dict(self) -> dict[str, object]:
        args: list[Expr] = []
        for arg in self.args:
            args.append(arg.to_dict())

        return {
            "fun-call": {
                "name": self.name.to_dict(),
                "args": args
            }
        }

@dataclass
class FloxTrue:
    token: Token

    def to_dict(self) -> dict[str, object]:
        return "true"

@dataclass
class FloxFalse:
    token: Token

    def to_dict(self) -> dict[str, object]:
        return "false"

class Null(Expr):
    token: Token

    def __init__(self, token: Token = None):
        if token:
            self.token = token
        else:
            self.token = fake_token()
    
    def to_dict(self) -> dict[str, object]:
        return "null"