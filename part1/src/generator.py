from typing import List, Set
from .grammar import Grammar, Rule
MAX_DEPTH = 10
def is_terminal(sym: str) -> bool:
    return sym.startswith("\"") and sym.endswith("\"")
def strip_quotes(sym: str) -> str:
    return sym[1:-1] if is_terminal(sym) else sym
def _expand(grammar: Grammar, sent: List[str], max_depth: int, results: List[List[str]]
            , max_sentences: int):
    if len(results) >= max_sentences:
        return
    if max_depth <= 0:
        return

    for i, sym in enumerate(sent):
        if not is_terminal(sym):
            for rule in grammar.index_by_lhs.get(sym, []):
                new_sent = sent[:i] + rule.rhs + sent[i + 1:]
                _expand(grammar, new_sent, max_depth - 1, results, max_sentences)
            return
    results.append(sent)
def generate_sentences(grammar: Grammar, max_sentences: int = 10000) -> List[str]:
    results: List[List[str]] = []
    _expand(grammar, [grammar.start_symbol], MAX_DEPTH, results, max_sentences)
    return [" ".join(strip_quotes(tok) for tok in s) for s in results]
