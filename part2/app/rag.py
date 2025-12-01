import json
import os
import re
from typing import List, Dict, Tuple

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "menu.json")

def load_menu() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def tokenize(text: str) -> set:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9À-ỹ\s]", " ", text)
    tokens = text.split()
    return set(tokens)

def build_docs(menu: List[Dict]) -> List[Tuple[str, Dict]]:
    docs = []
    for item in menu:
        doc = (
            f"Tên món: {item['name']}. "
            f"Giá: {item['price']} đồng. "
            f"Loại: {item.get('category', '')}. "
            f"Tùy chọn: {', '.join(item.get('options', []))}. "
            f"Tình trạng: {'còn món' if item.get('available', False) else 'hết món'}. "
            f"Mô tả: {item.get('description', '')}"
        )
        docs.append((doc, item))
    return docs

def retrieve_relevant_docs(query: str, k: int = 3) -> List[Tuple[str, Dict]]:
    menu = load_menu()
    docs = build_docs(menu)
    q_tokens = tokenize(query)
    scored = []
    for doc_text, item in docs:
        d_tokens = tokenize(doc_text)
        inter = len(q_tokens & d_tokens)
        union = len(q_tokens | d_tokens) or 1
        score = inter / union
        scored.append((score, doc_text, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [(doc, item) for score, doc, item in scored[:k] if score > 0]
    return top

def format_menu_for_llm() -> str:
    """
    Trả về chuỗi mô tả toàn bộ menu – dùng cho intent 'xem menu'.
    """
    menu = load_menu()
    lines = []
    for item in menu:
        status = "còn món" if item.get("available", False) else "tạm hết"
        line = f"- {item['name']} ({item['price']}đ, {status})"
        lines.append(line)
    return "\n".join(lines)