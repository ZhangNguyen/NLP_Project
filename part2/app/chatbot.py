from .intents import detect_intent, extract_quantity_and_item
from .order_manager import OrderManager
from .llm_client import LLMClient
from .rag import retrieve_relevant_docs, format_menu_for_llm
import json
import re


class FoodChatbot:
    def __init__(self):
        self.menu = json.load(open("data/menu.json", encoding="utf8"))
        self.orders = OrderManager()
        self.llm = LLMClient()
        self.history = []
        self.delivery_time = None

    def handle(self, message):
        intent, detected_item = detect_intent(message, self.menu)
        result = extract_quantity_and_item(message)
        item = result.get("item_name")
        qty = result.get("quantity")
        # RAG lấy thông tin menu liên quan
        docs = retrieve_relevant_docs(message)

        # ======== XỬ LÝ HÀNH ĐỘNG THẬT ========

        # Đặt món
        if intent == "order_food" and item:
            self.orders.add_item(item, qty)
            action_result = f"Đã thêm {qty} {item} vào đơn."

        # Thêm món
        elif intent == "add_item" and item:
            self.orders.add_item(item, qty)
            action_result = f"Đã thêm {qty} {item}."

        # Hủy món
        elif intent == "cancel_item" and item:
            self.orders.remove_item(item)
            action_result = f"Đã hủy món {item}."

        # Thay đổi số lượng
        elif intent == "update_quantity" and item:
            self.orders.update_quantity(item, qty)
            action_result = f"Đã cập nhật {item} thành {qty} phần."

        # Xem đơn hàng
        elif intent == "ask_order":
            action_result = self.orders.summary_text()

        # Đặt thời gian giao hàng
        elif intent == "schedule_delivery":
            self.delivery_time = message
            action_result = "Dạ em đã ghi nhận thời gian giao hàng ạ."

        else:
            action_result = None

        # ===== Gửi sang LLM để tạo câu trả lời tự nhiên =====

        reply = self.llm.generate({
            "intent": intent,
            "menu_item": item,
            "price": self.menu[item]["price"] if item in self.menu else None,
            "docs": docs,
            "action_result": action_result,
            "user_message": message,
            "history": self.history,
            "order_summary": self.orders.summary_text(),
            "delivery_time": self.delivery_time
        })

        self.history.append({"user": message})
        self.history.append({"bot": reply})
        return reply
