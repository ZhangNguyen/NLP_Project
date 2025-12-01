from typing import List, Dict


class OrderManager:
    def __init__(self):
        self.items: List[Dict] = []
        self.last_item_name: str | None = None

    def add_item(self, name: str, quantity: int = 1):
        for it in self.items:
            if it["name"] == name:
                it["quantity"] += quantity
                self.last_item_name = name
                return
        self.items.append({"name": name, "quantity": quantity, "options": ""})
        self.last_item_name = name

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
            opt = it.get("options") or ""
            if opt:
                lines.append(f"- {it['quantity']} x {it['name']} ({opt})")
            else:
                lines.append(f"- {it['quantity']} x {it['name']}")
        return "Các món bạn đã đặt:\n" + "\n".join(lines)

    def update_quantity(self, name, qty):
        for it in self.items:
            if it["name"] == name:
                it["quantity"] = qty
                return True
        return False

    def get_last_item_name(self) -> str | None:
        return self.last_item_name

    def update_option(self, name: str, option_text: str) -> bool:
        for it in self.items:
            if it["name"] == name:
                it["options"] = option_text
                return True
        return False

    def summary_with_total(self, menu: list[dict]) -> str:
        """
        Trả về text liệt kê các món + tổng tạm tính.
        menu: list các dict món trong menu.json
        """
        if not self.items:
            return "Hiện tại bạn chưa đặt món nào."

        lines = []
        total = 0

        for it in self.items:
            # tìm giá trong menu
            price = None
            for m in menu:
                if m["name"].lower() == it["name"].lower():
                    price = m.get("price", 0)
                    break

            opt = it.get("options") or ""
            price_part = f" ({price}đ/phần)" if price is not None else ""

            if opt:
                lines.append(f"- {it['quantity']} x {it['name']} ({opt}){price_part}")
            else:
                lines.append(f"- {it['quantity']} x {it['name']}{price_part}")

            if price is not None:
                total += it["quantity"] * price

        lines.append(f"Tổng tạm tính: {total}đ")
        return "Các món bạn đã đặt:\n" + "\n".join(lines)
