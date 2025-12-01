import requests
import os

class LLMClient:
    def __init__(self):
        self.endpoint = os.environ.get("LLM_ENDPOINT", "http://localhost:11434")

    def generate(self, context: dict):

        action_part = context.get("action_result") or ""

        prompt = f"""
        Bạn là nhân viên phục vụ nhà hàng, trả lời tự nhiên nhưng phải DỰA 100% vào dữ liệu thật bên dưới.
        Tuyệt đối KHÔNG được tự bịa món ăn, tên món hay giá món.

        NGÔN NGỮ:
        - Trả lời 100% Tiếng Việt trong tất cả cuộc hội thoại.
        - Tuyệt đối không dùng tiếng Trung hay tiếng Anh.
        - Nếu khách gõ tiếng Việt lẫn tiếng Anh, vẫn trả lời hoàn toàn bằng tiếng Việt.

        ================= DỮ LIỆU MENU (RAG) =================
        {context.get('menu')}

        ================= HÀNH ĐỘNG ĐÃ XỬ LÝ =================
        {action_part}

        ================= NGỮ CẢNH =================
        Intent: {context.get('intent')}
        Món khách hỏi: {context.get('menu_item')}
        Giá món: {context.get('price')}
        Đơn hàng hiện tại: {context.get('order_summary')}
        Thời gian giao hàng: {context.get('delivery_time')}

        ================= YÊU CẦU TRẢ LỜI =================
        - Trả lời NGẮN GỌN, tự nhiên, thân thiện.
        - Dựa vào hành động xử lý, xác nhận lại yêu cầu của khách hàng một cách tự nhiên.
        - Xưng hô với khách hàng là bạn, còn xưng hô chính mình là tôi
        - Tập trung dựa vào ngữ cảnh để trả lời dữ liệu một cách chính xác
        - Nếu dữ liệu RAG có món → chỉ được dùng đúng thông tin đó.
        - Nếu RAG không tìm thấy món → nói “bên em không có món này trong menu”.
        - Không được tự bịa món mới.
        - Không được chế biến mô tả sai menu. Nếu khách hỏi menu, phải liệt kê toàn bộ các món có trong menu.
        - Không được trả lời lan man.
        - Nếu action_result có nội dung → Hãy dùng nó để trả lời một cách tự nhiên trước tiên.
        Tin nhắn khách: "{context.get('user_message')}"
        """

        data = {
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }

        res = requests.post(f"{self.endpoint}/api/generate", json=data)
        return res.json()["response"].strip()
