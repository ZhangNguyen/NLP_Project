from dataclasses import dataclass
from typing import List, Dict, Tuple
import json
from pathlib import Path

Symbol = str
@dataclass()
class Rule:
    lhs: Symbol
    rhs: List[Symbol]

    def to_text(self):
        return f"{self.lhs} -> {' '.join(self.rhs)}"

class Grammar:
    def __init__(self,start_symbol: Symbol, rules: List[Rule]):
        self.start_symbol = start_symbol
        self.rules = rules
        self.index_by_lhs: Dict[Symbol, List[Rule]] = {}
        for r in rules:
            self.index_by_lhs.setdefault(r.lhs, []).append(r)

    @staticmethod
    def from_json(path: Path) -> "Grammar":
        data = json.loads(path.read_text(encoding="utf-8"))
        start_symbol = data["start"]
        rules = [Rule(lhs=r["lhs"], rhs=r["rhs"]) for r in data["rules"]]
        return Grammar(start_symbol, rules)

    def to_text(self) -> str:
        lines = [f"START {self.start_symbol}"]
        for r in self.rules:
            lines.append(r.to_text())
        return "\n".join(lines)




