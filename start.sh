#!/bin/sh
set -e

until python -c "
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings
try:
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
except Exception:
    sys.exit(1)
"; do
  echo "Waiting for postgres..."
  sleep 2
done

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
