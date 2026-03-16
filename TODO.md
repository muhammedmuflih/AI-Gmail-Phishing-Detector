# Fix Render Deployment: Gunicorn Worker Class Mismatch

## Plan Overview
Replace the Render `eventlet` worker setup with a threaded Gunicorn setup that matches the Flask-SocketIO app configuration.

## Steps to Complete

### ☐ 1. Update requirements.txt
Replace `eventlet` with `simple-websocket==1.0.0`

### ☐ 2. Update Procfile
Change `worker-class eventlet` to `worker-class gthread`

### ☐ 3. Update render.yaml
Change the `startCommand` from `worker-class eventlet` to `worker-class gthread`

### ☐ 4. Update gunicorn.conf.py
Set `worker_class = 'gthread'` and configure `threads`

### ☐ 5. Install dependencies
`pip install -r requirements.txt`

### ☐ 6. Local test with gthread
`gunicorn --worker-class gthread --threads 8 --bind 0.0.0.0:5000 app:app`

### ☐ 7. Commit and deploy
`git add gunicorn.conf.py Procfile render.yaml requirements.txt TODO.md && git commit -m "Fix Render deployment worker config" && git push origin main`

### ☐ 8. Verify Render deployment
Check Render dashboard/logs for successful start

## Status: Ready to execute step-by-step

**Next Action:** Commit the worker configuration changes and push to GitHub.
