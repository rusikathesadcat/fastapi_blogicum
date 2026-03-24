# Используем официальный образ Python 3.12 (cgi доступен в stdlib)
FROM python:3.12-slim

# Метаданные
LABEL maintainer="Meshastick"
LABEL description="FastAPI Blogicum deployment with Python 3.12 + cgi support"

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка системных зависимостей (если потребуются для сборки)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем только requirements.txt для эффективного кэширования слоёв
COPY requirements.txt .

# Установка зависимостей из requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Создаём пользователя для запуска приложения (безопасность)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Порт, который слушает Uvicorn
EXPOSE 8000

# Healthcheck для оркестраторов (опционально, но полезно)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Запуск приложения через Uvicorn
# --host 0.0.0.0 обязателен для доступа извне контейнера
# В production уберите --reload и рассмотрите использование gunicorn + uvicorn workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]