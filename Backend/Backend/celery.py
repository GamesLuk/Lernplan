from celery import Celery

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')  # <-- Ersetze "Backend" mit deinem Projekt-Namen

app = Celery("Backend")  # <-- Ersetze "Backend" mit deinem Projekt-Namen
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatisch Tasks aus `tasks.py` in Apps laden
app.autodiscover_tasks()

# Windows Fix: `solo` Mode nutzen, weil `fork()` nicht verfügbar ist
app.conf.worker_pool = 'solo'




from celery.schedules import crontab

