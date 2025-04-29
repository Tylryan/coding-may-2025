from __future__ import annotations

class LoxCallable:
    def arity(self) -> int:
        pass
    def call(self, interpreter, arguments: list[object]) -> object:
        pass