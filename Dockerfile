FROM python:3.13-alpine

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apk add --no-cache libpq-dev gcc musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic ./alembic
COPY alembic.ini .
COPY app ./app
COPY start.sh .

RUN chmod +x ./start.sh

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "./start.sh"]
