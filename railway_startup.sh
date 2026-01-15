#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "==> Running Migrations..."
python manage.py migrate --no-input

echo "==> Checking for Superuser..."
# This will create an admin user only if it doesn't exist
# It uses environment variables: ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
password = os.environ.get('ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username, email, password)
else:
    print(f"Superuser {username} already exists.")
END

echo "==> Starting Gunicorn..."
gunicorn starlinkdirect.wsgi --timeout 120 --workers 3 --threads 2
