# Sử dụng hình ảnh Python làm cơ sở
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép các tệp cần thiết vào container
COPY requirements.txt .

# Cài đặt các gói cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn của ứng dụng
COPY . .

# Tải xuống dữ liệu NLTK cần thiết
RUN python -m nltk.downloader punkt

# Chạy train.py trước khi chạy app.py
RUN python train.py

# Chạy ứng dụng Flask
CMD ["python", "app.py"]
