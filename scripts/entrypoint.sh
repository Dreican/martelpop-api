#!/usr/bin/env sh
set -e

echo "Waiting for the database"

until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER}" -d "${DB_NAME}"
do
  echo "PostgreSQL is unavailable - sleeping..."
  sleep 2
done

echo "PostgreSQL is ready."

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI..."
if [ "$UVICORN_RELOAD" = "true" ]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --no-access-log
else
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --no-access-log
fi