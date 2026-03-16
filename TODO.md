# Fix Render Deployment: Eventlet Worker Class Error

## Plan Overview
Add eventlet dependency and update gunicorn configs for Render compatibility.

## Steps to Complete

### ☐ 1. Update requirements.txt
Add `eventlet>=0.24.1`

### ☐ 2. Update Procfile  
Change `worker-class gthread` → `worker-class eventlet`

### ☐ 3. Update render.yaml
Change `startCommand` `worker-class gthread` → `worker-class eventlet`

### ☐ 4. Update gunicorn.conf.py
Set `worker_class = 'eventlet'`, `workers=1`

### ☐ 5. Install dependencies
`pip install -r requirements.txt`

### ☐ 6. Local test with eventlet
`gunicorn --worker-class eventlet --bind 0.0.0.0:5000 app:app`

### ☐ 7. Commit and deploy
`git add . && git commit -m "Fix Render deployment: add eventlet worker" && git push`

### ☐ 8. Verify Render deployment
Check Render dashboard/logs for successful start

## Status: Ready to execute step-by-step

**Next Action:** Update requirements.txt (Step 1)
