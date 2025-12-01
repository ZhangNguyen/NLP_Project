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
        def find_item_from_docs(message, docs):
            msg = message.lower()

            best_item = None
            for doc_text, meta in docs:
                name = (meta or {}).get("name", "")
                if name and name.lower() in msg:
                    best_item = name
                    break

            return best_item
        # ===== 1. Nhận diện intent + món, số lượng =====
        # danh sách tên món để detect_intent (tránh lỗi 'dict' không có lower)
        intent, _ = detect_intent(message, self.menu)
        docs = retrieve_relevant_docs(message)

        parsed = extract_quantity_and_item(message)
        item = find_item_from_docs(message, docs)
        qty = parsed.get("quantity") or 1
        action_result = None

        # ===== 2. Lấy dữ liệu menu cho LLM (RAG) =====
        # Nếu hỏi menu → đưa toàn bộ menu cho LLM, tránh bịa thêm món
        menu = format_menu_for_llm()
        if intent == "ask_menu":
            action_result = f"Dạ, menu của bên em bao gồm {menu}"
        # Hủy món
        elif intent == "cancel_item" and item:
            self.orders.remove_item(item)
            action_result = f"Đã hủy món {item}."
            # Cập nhật số lượng
        elif intent == "update_quantity" and item:
            self.orders.update_quantity(item, qty)
            action_result = f"Đã cập nhật {item} thành {qty} phần."
        # Đặt món mới
        elif intent == "order_food" and item:
            # Tìm món trong menu
            for m in self.menu:
                if m["name"].lower() == item.lower():
                    item_info = m
                    break

            if item_info is None:
                # Không có món này trong menu
                action_result = f"Dạ, bên em không có món {item} trong menu ạ."
            elif not item_info.get("available", False):
                # Có món nhưng đang hết
                action_result = f"Dạ, món {item_info['name']} hiện đang tạm hết, anh/chị chọn giúp em món khác nhé."
            else:
                # Món hợp lệ & còn hàng → cho vào giỏ
                self.orders.add_item(item_info["name"], qty)
                action_result = f"Đã thêm {qty} x {item_info['name']} vào đơn."
        elif intent == "ask_price" and not item:
            last = self.orders.get_last_item_name()
            if last:
                item = last


        # Cập nhật tùy chọn (ít đá, ít đường, ít hành…)
        elif intent == "update_option":
            # Nếu user không nhắc lại tên món → lấy món đặt gần nhất
            target_item = item or self.orders.get_last_item_name()
            if target_item:
                # Lưu nguyên câu nói làm phần options (ví dụ: "ít đá", "ít hành, nhiều nước")
                self.orders.update_option(target_item, message)
                item = target_item
                action_result = f"Đã ghi nhận yêu cầu “{message}” cho món {target_item}."
            else:
                action_result = "Hiện tại bạn chưa có món nào trong đơn để chỉnh sửa ạ."

        # Xem đơn hàng
        elif intent == "ask_order":
            action_result = self.orders.summary_with_total(self.menu)

        # Ghi nhận thời gian giao hàng
        elif intent == "schedule_delivery":
            self.delivery_time = message
            action_result = "Dạ em đã ghi nhận thời gian giao hàng ạ."

        # ===== 4. Tìm lại đúng price theo menu.json =====
        price = None
        canonical_name = item
        if item:
            for m in self.menu:
                if m["name"].lower() == item.lower():
                    canonical_name = m["name"]
                    price = m.get("price")
                    break

        # ===== 5. Gửi sang LLM để tạo câu trả lời tự nhiên =====
        reply = self.llm.generate({
            "intent": intent,
            "menu_item": canonical_name,
            "price": price,
            "docs": docs,
            "action_result": action_result,
            "user_message": message,
            "history": self.history,
            "order_summary": self.orders.summary_with_total(self.menu),
            "delivery_time": self.delivery_time,
            "menu": menu,
        })

        # Lưu lịch sử hội thoại
        self.history.append({"user": message})
        self.history.append({"bot": reply})

        return reply

