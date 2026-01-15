# Deployment Guide: Starlinkdirect on Render (Free Tier)

This guide walks you through deploying your **Starlinkdirect** Django application to Render's free tier. The codebase has already been prepared with the necessary configuration files.

## 1. Render Account Setup
1.  Go to [dashboard.render.com/register](https://dashboard.render.com/register).
2.  Sign up using your **GitHub** or **GitLab** account (recommended for easy repository connection).
3.  Verify your email to activate the account.

## 2. Code Preparation (Already Completed)
The following changes have been made to your codebase to support deployment:
*   **`requirements.txt`**: Added `gunicorn`, `whitenoise`, `dj-database-url`, and `psycopg2-binary`.
*   **`starlinkdirect/settings.py`**:
    *   Configured `ALLOWED_HOSTS` to accept Render's domain.
    *   Added `WhiteNoise` for serving static files.
    *   Configured `DATABASES` to switch between SQLite (local) and PostgreSQL (Render) automatically.
*   **`Procfile`**: Created to tell Render how to run the app (`web: gunicorn starlinkdirect.wsgi`).
*   **`build.sh`**: Created to handle dependency installation, static file collection, and database migrations.

**Action Required:**
1.  Commit and push these changes to your GitHub/GitLab repository.
    ```bash
    git add .
    git commit -m "Prepare for Render deployment"
    git push origin main
    ```

## 3. Deployment Process

### Step A: Create a Database
Since the free PostgreSQL database on Render expires after 90 days (previously 30), it is good for initial testing.
1.  In the Render Dashboard, click **New +** -> **PostgreSQL**.
2.  **Name**: `starlinkdirect-db` (or similar).
3.  **Region**: Choose the one closest to your users (e.g., Frankfurt or Singapore).
4.  **Instance Type**: Select **Free**.
5.  Click **Create Database**.
6.  **Wait** for the database to initialize. Once plain text is available, copy the **Internal Database URL** (it looks like `postgres://user:password@hostname/dbname`).

### Step B: Create the Web Service
1.  Click **New +** -> **Web Service**.
2.  Connect your GitHub/GitLab repository.
3.  **Name**: `starlinkdirect` (This will determine your URL, e.g., `starlinkdirect.onrender.com`).
4.  **Region**: Same as your database.
5.  **Branch**: `main` (or master).
6.  **Runtime**: **Python 3**.
7.  **Build Command**: `./build.sh`
8.  **Start Command**: `gunicorn starlinkdirect.wsgi`
9.  **Instance Type**: **Free**.
10. **Environment Variables** (Click "Advanced" or scroll down):
    *   Add `PYTHON_VERSION`: `3.11.5` (or your local version).
    *   Add `SECRET_KEY`: (Generate a strong random string).
    *   Add `DEBUG`: `False` (Important for security).
    *   Add `DATABASE_URL`: Paste the **Internal Database URL** you copied earlier.
    *   Add `PAYHERO_API_USERNAME`, `PAYHERO_API_PASSWORD`, etc., from your local `.env` file.
11. Click **Create Web Service**.

## 4. Handling Callbacks & Uptime (Critical)
Render's free web services **spin down (sleep)** after 15 minutes of inactivity. This creates a delay (approx. 50s-1min) when a new request comes in.

**Problem:** If M-Pesa sends a payment notification (callback) while the app is sleeping, the request might time out or fail before the app wakes up.

**Solution: usage of Uptime Monitoring**
To keep your app "warm" and ready for callbacks:
1.  Sign up for a free account at **[UptimeRobot](https://uptimerobot.com/)**.
2.  Click **Add New Monitor**.
3.  **Monitor Type**: HTTP(s).
4.  **Friendly Name**: Starlinkdirect.
5.  **URL**: Your Render URL (e.g., `https://starlinkdirect.onrender.com/`).
6.  **Monitoring Interval**: **5 minutes** (This prevents the 15-minute sleep cycle).
7.  Click **Create Monitor**.

## 5. Verification & Troubleshooting
1.  **Check Logs**: In the Render Dashboard, click on your Web Service and view the **Logs** tab. Watch for "deployed successfully" and "Listening at: http://0.0.0.0:10000".
2.  **Visit URL**: Go to your `.onrender.com` URL. You should see the Starlinkdirect homepage.
3.  **Test Payment**: Try initiating a small transaction. Check the logs to see if the callback is received.

### Common Issues
*   **Static Files Not Loading**: Ensure `WhiteNoise` is in `MIDDLEWARE` in `settings.py` (we added this).
*   **Database Errors**: Ensure `DATABASE_URL` is correct and migrations ran during the build (controlled by `build.sh`).
*   **Allowed Hosts Error**: Ensure `RENDER_EXTERNAL_HOSTNAME` is being picked up or your URL is in `ALLOWED_HOSTS`.
