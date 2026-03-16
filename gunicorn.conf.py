import os

bind = "0.0.0.0:" + os.getenv('PORT', '5000')
workers = 1
worker_class = "gthread"
threads = int(os.getenv("GUNICORN_THREADS", "8"))
timeout = 300
keepalive = 2
loglevel = "error"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
