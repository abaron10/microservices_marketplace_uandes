import multiprocessing
import os

wsgi_app = "app:gunicorn()"
bind = f"0.0.0.0:{os.environ.get('FLASK_PORT', '3020')}"

# Numero de workers
workers = multiprocessing.cpu_count() * 2 + 1

timeout = 200