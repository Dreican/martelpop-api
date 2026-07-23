#!/usr/bin/env sh
set -e

echo "Waiting for the database"

until pg_isready -h "${DB__HOST:-db}" -p "${DB__PORT:-5432}" -U "${DB__USER}" -d "${DB__NAME}"
do
  echo "PostgreSQL is unavailable - sleeping..."
  sleep 2
done

echo "PostgreSQL is ready."

if [ "$ALEMBIC_AUTO_UPGRADE" = "true" ]; then
  echo "Running database migrations..."
  alembic upgrade head
else
  echo "Alembic auto upgrade off"
fi

echo "Starting FastAPI..."
if [ "$UVICORN_RELOAD" = "true" ]; then
  exec uvicorn app.main:app --host "${APP__HOST}" --port "${APP__PORT}" --reload --no-access-log
else
  exec uvicorn app.main:app --host "${APP__HOST}" --port "${APP__PORT}" --no-access-log
fi