from typing import List, Tuple, Optional
from .grammar import Grammar, Rule

def is_terminal(sym: str) -> bool:
    return sym.startswith("\"") and sym.endswith("\"")

def strip_quotes(s: str) -> str:
    return s[1:-1] if is_terminal(s) else s

class ParseFailure(Exception):
    pass

def parse_sentence(grammar: Grammar, sentence: str) -> Optional[str]:
    tokens = sentence.strip().split()
    n = len(tokens)

    def parse_symbol(sym: str, pos: int) -> Tuple[int, str]:
        if is_terminal(sym):
            word = strip_quotes(sym)
            if pos < n and tokens[pos] == word:
                return pos + 1, f"{word}"
            else:
                raise ParseFailure

        for rule in grammar.index_by_lhs.get(sym, []):
            cur_pos = pos
            children_trees: List[str] = []
            try:
                for s in rule.rhs:
                    cur_pos, t = parse_symbol(s, cur_pos)
                    children_trees.append(t)
                return cur_pos, f"({sym} {' '.join(children_trees)})"
            except ParseFailure:
                continue
        raise ParseFailure
    try:
        end_pos, tree = parse_symbol(grammar.start_symbol, 0)
        if end_pos == n:
            return tree
        else:
            # parse không cover hết token
            return None
    except ParseFailure:
        return None
