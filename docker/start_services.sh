#!/bin/bash

# Start Caddy
echo "Starting Caddy..."
caddy run --config /app/Webserver/Caddyfile &

# Start Django
echo "Starting Django..."
cd /app/Backend
python3 manage.py runserver 0.0.0.0:8000 &

# Start Celery
echo "Starting Celery..."
celery -A Backend.celery worker --loglevel=info &

# Start Celery Beat
echo "Starting Celery Beat..."
celery -A Backend.celery beat --loglevel=info &

# Wait for all background processes to finish
wait
