#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# Run database migrations to create all database tables
python manage.py migrate

# Seed initial platform data (events, challenges, technical hubs, etc.)
python manage.py seed_data

# Create a superuser automatically on first deploy if DJANGO_SUPERUSER_* vars are set.
# Set these in Render's Environment tab:
#   DJANGO_SUPERUSER_USERNAME
#   DJANGO_SUPERUSER_EMAIL
#   DJANGO_SUPERUSER_PASSWORD
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
        2>/dev/null || echo "Superuser already exists — skipping creation."
fi
