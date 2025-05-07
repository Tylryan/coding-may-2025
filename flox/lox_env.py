from __future__ import annotations

from tokens import Token
from exprs import Expr

class Env:
    symbol_table: dict[str, object]
    parent: Env

    def __init__(self, parent: Env):
        self.symbol_table = {}
        self.parent  = parent

    def define(self, name: Token, value: object) -> None: 
        assert isinstance(name, Token)
        self.symbol_table[name.lexeme] = value

    def assign(self, name: Token, value: object) -> None: 
        assert isinstance(name, Token)
        if name.lexeme in self.symbol_table.keys():
            self.symbol_table[name.lexeme] = value
            return None
        
        if self.parent:
            return self.parent.assign(name, value)
        
        print(f"[environment-error] cannot assign to an undefined variable "
              f"'{name.lexeme}' on line {name.line}.")
        exit(1)

    def get(self, name: Token) -> Expr: 
        if name.lexeme in self.symbol_table.keys():
            return self.symbol_table[name.lexeme]
        
        if self.parent:
            return self.parent.get(name)
        
        print(f"[environment-error] undefined variable "
              f"'{self.name.lexeme}' on line {self.name.line}.")
        exit(1)
