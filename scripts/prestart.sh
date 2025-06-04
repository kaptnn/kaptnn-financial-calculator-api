#!/usr/bin/env sh
set -e
set -x

host="$DB_HOST"
port="${DB_PORT:-3306}"

echo "⏳ Waiting for MySQL at $host:$port..."

until nc -z "$host" "$port"; do
  sleep 1
done

echo "✅ MySQL is up - executing command"
exec "$@"

echo "🚀 Running Alembic migrations..."
alembic upgrade head

echo "🌱 Seeding superadmin user..."
python -m app.utils.seed

echo "🔥 Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
