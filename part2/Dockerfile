FROM python:3.10-slim

# 1. Tắt buffer để log ra ngay
ENV PYTHONUNBUFFERED=1

# 2. Làm việc trong /app
WORKDIR /app

# 3. Cài lib Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy toàn bộ source vào container
COPY . .

# 5. Biến môi trường cho Flask (dùng factory create_app trong app/web.py)
ENV FLASK_APP=app.web:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

EXPOSE 8000

# 6. Lệnh chạy chính
CMD ["flask", "run"]
