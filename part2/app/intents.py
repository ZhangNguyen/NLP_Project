import re
from typing import Dict

INTENT_KEYWORDS = {
    "ask_menu": [r"menu", r"món nào", r"danh sách món", r"những món gì", r"có món gì", r"thực đơn"],
    "ask_price": [r"bao nhiêu", r"giá", r"bao nhieu", r"bao tiền"],
    "order_food": [r"đặt", r"order", r"mua", r"cho tôi","thêm", r"add", r"gọi", r"cho mình","cho","bán"],
    "cancel_item": [r"hủy", r"huy", r"bỏ", r"xóa"],
    "ask_order": [r"đơn", r"đã đặt", r"đang đặt gì", r"order", r"lịch sử đơn", r"đã đặt những món gì"],
    "schedule_delivery": [r"giao lúc", r"giao vào", r"giờ giao", r"\d+h"],

    # ➜ update số lượng
    "update_quantity": [r"giảm xuống còn", r"bớt xuống", r"đổi còn", r"sửa lại số lượng", r"còn \d+ phần"],

    # ➜ update tuỳ chọn (ít đá, ít đường…)
    "update_option": [r"ít đá", r"nhiều đá", r"ít đường", r"nhiều đường",
                      r"ít hành", r"nhiều hành", r"ít nước", r"nhiều nước", r"trân châu","thêm chả","thêm bún"]
}

def detect_intent(text: str, menu=None):
    text_lower = text.lower()

    detected_intent = "unknown"
    for intent, patterns in INTENT_KEYWORDS.items():
        for p in patterns:
            if re.search(p, text_lower):
                detected_intent = intent

    # cố gắng tìm tên món
    found_item = None
    if menu:
        for item in menu:
            name = item.get("name", "").lower()  # lấy tên món
            if name and name in text_lower:
                found_item = item["name"]        # lưu lại tên món dạng string
                break

    return detected_intent, found_item



def extract_quantity_and_item(text: str) -> Dict:
    """
    Nhận dạng số lượng theo cả dạng số (1, 2, 3...)
    và dạng chữ tiếng Việt (một, hai, ba, bốn...).
    Ví dụ:
        '1 phần phở bò'
        'một tô bún'
        'hai ly trà sữa'
    """
    text_lower = text.lower().strip()

    # Mapping số tiếng Việt → số thật
    vn_numbers = {
        "một": 1, "một phần": 1,
        "hai": 2, "ba": 3, "bốn": 4, "tư": 4,
        "năm": 5, "sáu": 6, "bảy": 7,
        "tám": 8, "chín": 9, "mười": 10
    }

    result = {"quantity": 1, "item_name": None}

    # --- 1. Bắt dạng SỐ: "2 phần phở bò" ---
    m_digit = re.search(r"(\d+)\s*(phần|ly|tô|bát)?\s*([a-zA-ZÀ-ỹ\s]+)", text_lower)
    if m_digit:
        qty = int(m_digit.group(1))
        name = m_digit.group(3).strip()
        result["quantity"] = qty
        result["item_name"] = name
        return result

    # --- 2. Bắt dạng CHỮ: "một phần phở bò", "hai ly trà sữa" ---
    m_word = re.search(
        r"(một|hai|ba|bốn|tư|năm|sáu|bảy|tám|chín|mười)\s*(phần|ly|tô|bát)?\s*([a-zA-ZÀ-ỹ\s]+)",
        text_lower
    )
    if m_word:
        word = m_word.group(1)
        name = m_word.group(3).strip()
        qty = vn_numbers.get(word, 1)
        result["quantity"] = qty
        result["item_name"] = name
        return result

    # --- 3. Không có số lượng: trả quantity mặc định = 1 ---
    m_item_only = re.search(r"(phần|ly|tô|bát)?\s*([a-zA-ZÀ-ỹ\s]+)", text_lower)
    if m_item_only:
        name = m_item_only.group(2).strip()
        result["item_name"] = name

    return result
