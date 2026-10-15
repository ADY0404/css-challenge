# Production Dockerfile for Computer Science Society Platform on Fly.io
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install essential system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Make release and entrypoint scripts executable
RUN chmod +x /app/release.sh /app/entrypoint.sh

# Collect static files into STATIC_ROOT during build
RUN DJANGO_DEBUG=1 SECRET_KEY=build-dummy-key-for-collectstatic python manage.py collectstatic --noinput

# Expose standard Fly.io web port
EXPOSE 8000

# Run entrypoint script
CMD ["/app/entrypoint.sh"]

