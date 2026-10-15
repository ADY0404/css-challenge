#!/usr/bin/env bash
set -e

# Ensure data directory and media directory exist on mounted volume
mkdir -p /data /data/media

echo "==> [Fly.io Entrypoint] Running database migrations on persistent volume..."
python manage.py migrate --noinput

echo "==> [Fly.io Entrypoint] Seeding initial platform data..."
python manage.py seed_data

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "==> [Fly.io Entrypoint] Ensuring admin superuser exists..."
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" 2>/dev/null || echo "Superuser already exists."
fi

echo "==> [Fly.io Entrypoint] Starting Gunicorn web server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --threads 4 --access-logfile - --error-logfile - myfirst.wsgi:application

