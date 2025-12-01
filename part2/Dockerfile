# Image Python nhẹ
FROM python:3.10-slim

# Tạo thư mục làm việc trong container
WORKDIR /app

# Copy file requirements trước để pip install (tối ưu cache)
COPY requirements.txt .

# Cài các package Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Endpoint mặc định để gọi Ollama (sẽ override bằng ENV khi chạy)
ENV LLM_ENDPOINT=http://host.docker.internal:11434

# Flask chạy port 8000
EXPOSE 8000

# Chạy web server Flask
CMD ["python", "-m", "app.web"]
