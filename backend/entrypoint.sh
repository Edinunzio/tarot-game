#!/bin/sh
set -e

echo "Waiting for database..."
until python -c "import psycopg2; psycopg2.connect(
    dbname='${POSTGRES_DB}',
    user='${POSTGRES_USER}',
    password='${POSTGRES_PASSWORD}',
    host='${POSTGRES_HOST}',
    port='${POSTGRES_PORT}'
)" 2>/dev/null; do
  sleep 1
done
echo "Database ready."

python manage.py migrate --noinput

exec "$@"
