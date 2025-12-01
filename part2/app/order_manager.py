from typing import List, Dict


class OrderManager:
    def __init__(self):
        self.items: List[Dict] = []

    def add_item(self, name: str, quantity: int = 1):
        for it in self.items:
            if it["name"] == name:
                it["quantity"] += quantity
                return
        self.items.append({"name": name, "quantity": quantity})

    def remove_item(self, name: str):
        self.items = [it for it in self.items if it["name"] != name]

    def has_item(self, name: str) -> bool:
        """
        Kiểm tra xem món 'name' có tồn tại trong giỏ hàng không.
        Trả về True nếu có, False nếu không.
        """
        for it in self.items:
            if it["name"].lower() == name.lower():
                return True
        return False
    def summary_text(self) -> str:
        if not self.items:
            return "Hiện tại bạn chưa đặt món nào."
        lines = []
        for it in self.items:
            lines.append(f"- {it['quantity']} x {it['name']}")
        return "Các món bạn đã đặt:\n" + "\n".join(lines)

    def update_quantity(self, name, qty):
        for it in self.items:
            if it["name"] == name:
                it["quantity"] = qty
                return True
        return False
