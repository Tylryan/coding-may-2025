from __future__ import annotations
from dataclasses import dataclass

from exprs import Expr

@dataclass
class FloxReturn(RuntimeError):
    value: Expr