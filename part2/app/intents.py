import re
from typing import Dict

INTENT_KEYWORDS = {
    "ask_menu": [r"\bmenu\b", r"món nào", r"danh sách món", r"những món gì", r"có món gì", r"thực đơn"],
    "ask_price": [r"bao nhiêu", r"giá", r"bao nhieu", r"bao tiền"],
    "order_food": [r"đặt", r"cho tôi", r"order",r"mua"],
    "add_item": [r"thêm", r"gọi thêm", r"add"],
    "cancel_item": [r"hủy", r"huy mon", r"bỏ món", r"xóa món"],
    "ask_order": [r"đơn của tôi", r"tôi đã đặt", r"tôi đang đặt gì",r"order của tôi","lịch sử đơn"],
    "schedule_delivery": [r"giao lúc", r"giao vào", r"giờ giao", r"12h", r"18h"]
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
    tìm số và tên món dạng '2 phần phở bò'
    """
    text_lower = text.lower()
    m = re.search(r"(\d+)\s*(phần|ly|bát|tô)?\s*([a-zA-ZÀ-ỹ\s]+)", text_lower)
    result = {"quantity": 1, "item_name": None}
    if m:
        qty = m.group(1)
        name = m.group(3)
        try:
            result["quantity"] = int(qty)
        except ValueError:
            result["quantity"] = 1
        result["item_name"] = name.strip()
    return result