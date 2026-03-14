# Render Deployment Fix - TODO Steps

✅ **Step 1**: Create TODO.md (Done)

✅ **Step 2**: Optimize requirements.txt - Remove unused ML deps (numpy, pandas, scikit-learn, scipy, joblib) (Done)

✅ **Step 3**: Update render.yaml - Switch to gevent, preload, timeout 300 (Done)

✅ **Step 4**: Update app.py - Add /health endpoint, lazy imports, prod SocketIO config (Done)

✅ **Step 5**: Create Procfile and gunicorn.conf.py (Done)

**Step 6**: Local test with gunicorn gevent

**Step 7**: Commit and push to GitHub, trigger Render redeploy

**Progress**: 5/7 steps complete

**Step 6**: Local test with gunicorn gevent

**Step 7**: Commit and push to GitHub, trigger Render redeploy

**Progress**: 1/7 steps complete

**Status**: Optimizing for Render free tier (RAM <512MB, startup <15min)

