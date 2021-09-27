import os

CELERY_NAME = str(os.environ['CELERY_NAME']) if 'CELERY_NAME' in os.environ else 'main'
CELERY_BROKER = str(os.environ['CELERY_BROKER']) if 'CELERY_BROKER' in os.environ else 'redis://localhost:6379/0'
