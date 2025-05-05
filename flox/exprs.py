from __future__ import annotations

from dataclasses import dataclass

from tokens import Token

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