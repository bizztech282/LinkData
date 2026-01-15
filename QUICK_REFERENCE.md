# Starlinkdirect - Quick Reference Guide

## 🚀 Quick Start

### Local Development Setup

```bash
# 1. Navigate to project
cd c:/Users/Lenovo/Desktop/starlinkdirect-main

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file (see Environment Variables section)

# 6. Run migrations
python manage.py migrate

# 7. Create superuser (optional)
python manage.py createsuperuser

# 8. Run development server
python manage.py runserver

# 9. Access application
# Homepage: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
```

---

## 📋 Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - defaults to SQLite)
# DATABASE_URL=postgres://user:password@localhost/dbname

# PayHero API Configuration
PAYHERO_API_USERNAME=your_payhero_username
PAYHERO_API_PASSWORD=your_payhero_password
PAYHERO_API_URL=https://backend.payhero.co.ke/api/v2/payments
PAYHERO_CALLBACK_URL=https://yourdomain.com/api/mpesa/callback
PAYHERO_CHANNEL_ID=12345
BASIC_AUTH_TOKEN=your_basic_auth_token

# Optional
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=securepassword123
```

---

## 🔗 URL Routes

| URL | View | Template | Purpose |
|-----|------|----------|---------|
| `/` | `bundles.views.index` | `index.html` | Bundle selection page |
| `/payment/` | `bundles.views.payment` | `payment.html` | Payment page |
| `/api/stk-push/` | `bundles.views.initiate_stk` | - | STK Push API endpoint |
| `/api/mpesa/callback` | `bundles.views.mpesa_callback` | - | M-Pesa callback handler |
| `/admin/` | Django Admin | - | Admin interface |

---

## 💻 Common Django Commands

### Development

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on all interfaces
python manage.py runserver 0.0.0.0:8000

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell
```

### Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate bundles 0001

# Reset database (SQLite)
# Delete db.sqlite3 and run migrate again
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic

# Collect without prompts
python manage.py collectstatic --no-input

# Clear collected static files
python manage.py collectstatic --clear
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test bundles

# Run with verbose output
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

---

## 📦 Bundle Data

### Available Bundles

```python
# Daily Bundles
{
    "2GB": {"price": 150, "validity": "24 Hours"},
    "5GB": {"price": 299, "validity": "24 Hours"}
}

# Weekly Deals
{
    "8.75GB": {"price": 499, "validity": "7 Days"},
    "15GB": {"price": 850, "validity": "7 Days"}  # Recommended
}

# Monthly Value
{
    "25GB": {"price": 1500, "validity": "30 Days"},
    "50GB": {"price": 2500, "validity": "30 Days"}
}
```

---

## 🔌 API Reference

### POST /api/stk-push/

**Initiate STK Push Payment**

**Request:**
```json
{
  "phone_number": "0712345678",
  "recipient_phone": "0712345678",
  "amount": "150",
  "detail": "2GB (24Hrs)"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "STK Push sent successfully.",
  "data": {
    "transaction_id": "abc123",
    "reference": "TXN-A1B2C3D4"
  }
}
```

**Error Response (400/500):**
```json
{
  "success": false,
  "message": "Missing details."
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/stk-push/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "0712345678",
    "recipient_phone": "0712345678",
    "amount": "150"
  }'
```

### POST /api/mpesa/callback

**M-Pesa Payment Callback**

**Request (from PayHero):**
```json
{
  "ResultCode": 0,
  "ResultDesc": "Success",
  "ExternalReference": "TXN-A1B2C3D4",
  "TransactionID": "QA12BC34DE",
  "Amount": 150,
  "PhoneNumber": "254712345678"
}
```

**Response:**
```json
{
  "ResultCode": 0,
  "ResultDesc": "Accepted"
}
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

```bash
# Error: No module named 'django'
# Solution:
pip install -r requirements.txt
```

#### 2. Database Errors

```bash
# Error: no such table: django_session
# Solution:
python manage.py migrate
```

#### 3. Static Files Not Loading

```bash
# Error: Static files 404
# Solution (Development):
# Ensure DEBUG=True in settings

# Solution (Production):
python manage.py collectstatic
# Ensure WhiteNoise is in MIDDLEWARE
```

#### 4. CSRF Token Missing

```javascript
// Error: CSRF verification failed
// Solution: Include CSRF token in AJAX requests

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Use in fetch:
fetch('/api/stk-push/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data)
})
```

#### 5. PayHero API Errors

```python
# Error: Invalid channel_id
# Solution: Ensure PAYHERO_CHANNEL_ID is an integer

# Error: Authentication failed
# Solution: Check BASIC_AUTH_TOKEN format
# Should be: Basic base64(username:password)

# Error: Callback URL not reachable
# Solution: Use public URL (ngrok for local testing)
```

---

## 🧪 Testing with ngrok

For testing PayHero callbacks locally:

```bash
# 1. Install ngrok
# Download from https://ngrok.com/

# 2. Run Django server
python manage.py runserver

# 3. In another terminal, run ngrok
ngrok http 8000

# 4. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)

# 5. Update .env
PAYHERO_CALLBACK_URL=https://abc123.ngrok.io/api/mpesa/callback

# 6. Restart Django server
```

---

## 📊 Logging & Debugging

### View Logs

```python
# In views.py or payhero_api.py
import logging
logger = logging.getLogger(__name__)

# Log levels
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Console Logs

```bash
# Run server with verbose output
python manage.py runserver --verbosity=2

# View logs in real-time (production)
# Render: Dashboard → Logs tab
# Railway: Dashboard → Deployments → View Logs
```

### Django Debug Toolbar (Optional)

```bash
# Install
pip install django-debug-toolbar

# Add to settings.py INSTALLED_APPS
'debug_toolbar',

# Add to settings.py MIDDLEWARE
'debug_toolbar.middleware.DebugToolbarMiddleware',

# Add to settings.py
INTERNAL_IPS = ['127.0.0.1']

# Add to urls.py
import debug_toolbar
urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

---

## 🚀 Deployment Checklist

### Pre-Deployment

- [ ] Set `DEBUG=False`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `DATABASE_URL` (PostgreSQL)
- [ ] Configure all PayHero environment variables
- [ ] Set `PAYHERO_CALLBACK_URL` to production URL
- [ ] Test payment flow in sandbox
- [ ] Run `python manage.py check --deploy`
- [ ] Commit all changes to Git
- [ ] Push to GitHub/GitLab

### Render Deployment

```bash
# 1. Create PostgreSQL database
# Dashboard → New → PostgreSQL

# 2. Create Web Service
# Dashboard → New → Web Service
# Connect repository
# Build Command: ./build.sh
# Start Command: gunicorn starlinkdirect.wsgi

# 3. Set Environment Variables
# See Environment Variables section

# 4. Deploy
# Render will auto-deploy on git push
```

### Post-Deployment

- [ ] Check deployment logs
- [ ] Visit production URL
- [ ] Test bundle selection
- [ ] Test automatic payment (sandbox)
- [ ] Test manual payment flow
- [ ] Verify callback endpoint
- [ ] Set up UptimeRobot monitoring
- [ ] Test from mobile device
- [ ] Monitor error logs

---

## 🔐 Security Best Practices

### Development

```bash
# Never commit .env file
# Already in .gitignore

# Use strong SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Keep dependencies updated
pip list --outdated
pip install --upgrade package_name
```

### Production

- [ ] Use HTTPS only
- [ ] Set `DEBUG=False`
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Set `SECURE_SSL_REDIRECT=True`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Implement rate limiting
- [ ] Monitor failed login attempts
- [ ] Regular security audits

---

## 📱 Manual Payment Details

### Till Number
```
6944804
```

### WhatsApp Support
```
+254782070228
```

### Payment Instructions
1. M-Pesa → Lipa na M-Pesa → Buy Goods
2. Enter Till Number: 6944804
3. Enter Amount (e.g., Ksh 150)
4. Enter M-Pesa PIN
5. Send confirmation code via WhatsApp

---

## 🔄 Git Workflow

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push to main
git push origin main

# Create feature branch
git checkout -b feature/new-feature

# Merge feature branch
git checkout main
git merge feature/new-feature

# View logs
git log --oneline
```

---

## 📚 Useful Resources

### Django
- [Official Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

### PayHero
- [PayHero API Docs](https://payhero.co.ke/docs)
- [PayHero Dashboard](https://payhero.co.ke/dashboard)

### Deployment
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [WhiteNoise Docs](http://whitenoise.evans.io/)

### Frontend
- [Tailwind CSS](https://tailwindcss.com/)
- [Feather Icons](https://feathericons.com/)

---

## 🆘 Getting Help

### Check Logs
```bash
# Local
python manage.py runserver

# Production (Render)
# Dashboard → Service → Logs

# Production (Railway)
# Dashboard → Deployment → Logs
```

### Common Commands

```bash
# Check Django version
python -m django --version

# Check installed packages
pip list

# Check Python version
python --version

# Verify environment variables
python manage.py shell
>>> import os
>>> os.environ.get('SECRET_KEY')
```

### Debug Mode

```python
# In settings.py (DEVELOPMENT ONLY)
DEBUG = True
ALLOWED_HOSTS = ['*']

# View detailed error pages
# Visit the URL that's causing errors
```

---

## 📝 Code Snippets

### Create a New View

```python
# bundles/views.py
from django.shortcuts import render
from django.http import JsonResponse

def my_view(request):
    if request.method == 'GET':
        return render(request, 'my_template.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        # Process data
        return JsonResponse({'success': True})
```

### Add URL Pattern

```python
# bundles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my-url/', views.my_view, name='my_view'),
]
```

### Create Template

```html
<!-- bundles/templates/my_template.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Page</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```

### Make API Call

```python
# bundles/views.py
import requests

def call_external_api():
    url = "https://api.example.com/endpoint"
    headers = {"Authorization": "Bearer token"}
    payload = {"key": "value"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
```

---

## 🎯 Performance Tips

### Database Optimization

```python
# Use select_related for foreign keys
queryset = Transaction.objects.select_related('user')

# Use prefetch_related for many-to-many
queryset = Bundle.objects.prefetch_related('features')

# Add database indexes
class Transaction(models.Model):
    reference = models.CharField(max_length=50, db_index=True)
```

### Caching

```python
# Install Redis
pip install django-redis

# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Use cache
from django.core.cache import cache

cache.set('key', 'value', timeout=300)
value = cache.get('key')
```

### Static Files

```python
# Use CDN for static files (production)
# settings.py
STATIC_URL = 'https://cdn.example.com/static/'

# Compress static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

**Quick Reference Version:** 1.0  
**Last Updated:** January 15, 2026  
**For:** Starlinkdirect Development Team
