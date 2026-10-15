#!/usr/bin/env bash
# Release phase script executed automatically by Fly.io before new machines start
set -e

echo "==> [Fly.io Release] Running database migrations..."
python manage.py migrate --noinput

echo "==> [Fly.io Release] Seeding initial platform data..."
python manage.py seed_data

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "==> [Fly.io Release] Ensuring admin superuser exists..."
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" 2>/dev/null || echo "Superuser already exists."
fi

echo "==> [Fly.io Release] Release phase successfully completed!"

