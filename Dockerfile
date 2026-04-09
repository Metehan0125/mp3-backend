FROM python:3.11-slim

WORKDIR /app

# yt-dlp için gerekli sistem paketleri
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodları
COPY . .

# Flask backend'i başlat
CMD ["gunicorn", "app:app"]