# Chatbot Đặt Món Ăn – NLP Assignment 251 (Option 2: Chatbot + LLM/RAG)

MSSV: `...`  
Môn học: **Xử lý Ngôn ngữ Tự nhiên (CO3085)**  
Giảng viên: **Võ Thanh Hùng**

---

## 1. Mô tả bài toán

Hệ thống là một **chatbot đặt món ăn online**. Khách hàng có thể trò chuyện tự nhiên để:

- Xem menu  
- Hỏi giá từng món  
- Đặt món mới, thêm món  
- Hủy món trong đơn  
- Sửa số lượng  
- Ghi nhận yêu cầu đặc biệt (ít đường, ít đá, ít hành, thêm chả, …)  
- Ghi nhận thời gian giao hàng  
- Xem tóm tắt đơn hàng hiện tại  

Hệ thống sử dụng:

- Nhận diện intent (regex + rule-based)
- RAG dựa trên `menu.json`
- LLM (Qwen 2.5 – 7B) để sinh câu trả lời tự nhiên

Đây là triển khai cho **Lựa chọn 2: Chatbot đầy đủ với LLM/RAG** trong đề bài.

---

## 2. Kiến trúc & Thành phần chính

Thư mục nguồn chính: `app/`

- `menu.json`  
  Cơ sở dữ liệu menu giả lập (tên món, giá, category, options, trạng thái còn/hết).

- `rag.py`  
  Xây dựng tài liệu từ `menu.json` và truy vấn lại bằng một hàm retrieval đơn giản (Jaccard).
  - `retrieve_relevant_docs(query, k)` trả về top–k món liên quan.
  - `format_menu_for_llm()` trả về toàn bộ menu dạng text để đưa vào prompt.

- `intents.py`  
  - `INTENT_KEYWORDS`: tập regex để nhận diện các intent:  
    `ask_menu`, `ask_price`, `order_food`, `cancel_item`, `ask_order`,  
    `schedule_delivery`, `update_quantity`, `update_option`, …
  - `detect_intent(text, menu)` trả về `(intent, found_item)`.
  - `extract_quantity_and_item(text)` tách số lượng + tên món, hỗ trợ cả số (1, 2, 3) và chữ (một, hai, ba, …).

- `order_manager.py`  
  Quản lý giỏ hàng:
  - Thêm / xóa món
  - Cập nhật số lượng, cập nhật options
  - `summary_with_total(menu)` trả về text liệt kê từng món + tổng tiền.

- `llm_client.py`  
  Gọi LLM qua HTTP (mặc định tương thích API Ollama) bằng model `qwen2.5:7b`.
  - Sử dụng biến môi trường `LLM_ENDPOINT` để biết URL server LLM.
  - Build prompt gồm: dữ liệu menu (RAG), hành động đã xử lý, intent, đơn hàng hiện tại, thời gian giao hàng, câu người dùng.

- `chatbot.py`  
  Lớp `FoodChatbot` là “bộ não” của hệ thống.
  - Nhận diện intent + trích số lượng, tên món.
  - Gọi RAG (`retrieve_relevant_docs`) để tìm món liên quan.
  - Thực hiện hành động thật trên `OrderManager` (thêm món, hủy, sửa số lượng, cập nhật option, ghi nhận thời gian giao hàng).
  - Chuẩn hóa tên món + giá từ `menu.json`.
  - Gọi `LLMClient.generate()` để tạo câu trả lời tự nhiên dựa trên `action_result` + dữ liệu RAG.

- `web.py` – Flask app
  - `create_app()` khởi tạo Flask application.
  - Route `GET /` : giao diện web đơn giản (chat UI).
  - Route `POST /api/chat` : nhận `{ "message": "..." }` và trả về `{ "reply": "..." }`.

Ngoài ra có:

- `main.py` – chạy chatbot ở chế độ CLI (nhập từ terminal).

---

## 3. Yêu cầu hệ thống

### 3.1. Phần mềm cần có

Giảng viên cần:

1. **Docker**  
   - Đã cài Docker Desktop (Windows/macOS) hoặc Docker Engine (Linux).

2. **Kết nối internet** (lần đầu) để Docker tải image Ollama và model Qwen 2.5 7B.

> Trong README này, em hướng dẫn cài **Ollama bằng Docker** (không cần cài phần mềm Ollama riêng), và LLM sẽ lắng nghe tại:
> `http://localhost:11434`

### 3.2. Python packages (đã được cài trong Docker)

Các thư viện Python được liệt kê trong `requirements.txt`, ví dụ:

```txt
Flask==3.0.3
requests==2.32.3
python-dotenv==1.0.1

## 4. Hướng dẫn chạy

Mở **Terminal / PowerShell** tại thư mục gốc (thư mục chứa `Dockerfile`).

---

## 4.1. Bước 1 – Cài & chạy Ollama bằng Docker

### 4.1.1. Tải image Ollama

```bash
docker pull ollama/ollama
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull qwen2.5:7b

### 4.1.2 Build Docker image cho Chatbot
```bash
docker build -t foodbot-app .
docker run -d -p 8000:8000 -e LLM_ENDPOINT=http://host.docker.internal:11434 --name foodbot foodbot-app

### 4.1.3 Mở trình duyệt truy cập:
http://localhost:8000

