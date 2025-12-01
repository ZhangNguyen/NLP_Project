import requests
import os

class LLMClient:
    def __init__(self):
        self.endpoint = os.environ.get("LLM_ENDPOINT", "http://localhost:11434")

    def generate(self, context: dict):

        docs_text = ""
        if context.get("docs"):
            for doc, item in context["docs"]:
                docs_text += f"- {doc}\n"

        action_part = context.get("action_result") or ""

        prompt = f"""
    Bạn là nhân viên phục vụ nhà hàng, trả lời tự nhiên nhưng phải DỰA 100% vào dữ liệu thật bên dưới.
    Tuyệt đối KHÔNG được tự bịa món ăn, tên món hay giá món.

    ================= DỮ LIỆU MENU (RAG) =================
    {docs_text}

    ================= HÀNH ĐỘNG ĐÃ XỬ LÝ =================
    {action_part}

    ================= NGỮ CẢNH =================
    Intent: {context.get("intent")}
    Món khách hỏi: {context.get("menu_item")}
    Giá món: {context.get("price")}
    Đơn hàng hiện tại: {context.get("order_summary")}
    Thời gian giao hàng: {context.get("delivery_time")}

    ================= YÊU CẦU TRẢ LỜI =================
    - Trả lời NGẮN GỌN, tự nhiên, thân thiện.
    - Nếu dữ liệu RAG có món → chỉ được dùng đúng thông tin đó.
    - Nếu RAG không tìm thấy món → nói “bên em không có món này trong menu”.
    - Nếu action_result có nội dung → dùng nó để trả lời trước tiên (ví dụ: xác nhận đặt món).
    - Không được tự bịa món mới.
    - Không được chế biến mô tả sai menu. Nếu khách hỏi menu, phải liệt kê toàn bộ các món có trong menu
    - Không được trả lời lan man.

    Tin nhắn khách: "{context.get("user_message")}"
    """

        data = {
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }

        res = requests.post(f"{self.endpoint}/api/generate", json=data)
        return res.json()["response"].strip()
