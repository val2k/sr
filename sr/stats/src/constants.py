import os

CELERY_BROKER = str(os.environ['CELERY_BROKER']) if 'CELERY_BROKER' in os.environ else 'redis://localhost:6379/0'
CELERY_NAME = str(os.environ['CELERY_NAME']) if 'CELERY_NAME' in os.environ else 'main'

POSTGRES_DB = str(os.environ['POSTGRES_DB']) if 'POSTGRES_DB' in os.environ else 'postgres'
POSTGRES_HOST = str(os.environ['POSTGRES_HOST']) if 'POSTGRES_HOST' in os.environ else 'host.minikube.internal'
POSTGRES_PW = str(os.environ['POSTGRES_PW']) if 'POSTGRES_PW' in os.environ else 'postgres'
POSTGRES_USER = str(os.environ['POSTGRES_USER']) if 'POSTGRES_USER' in os.environ else 'postgres'

REDIS_PERSISTENT_DB = int(os.environ['REDIS_PERSISTENT_DB']) if 'REDIS_PERSISTENT_DB' in os.environ else 1
REDIS_PERSISTENT_HOST = str(os.environ['REDIS_PERSISTENT_HOST']) if 'REDIS_PERSISTENT_HOST' in os.environ else 'localhost'
REDIS_PERSISTENT_PORT = int(os.environ['REDIS_PERSISTENT_PORT']) if 'REDIS_PERSISTENT_PORT' in os.environ else 6379

WINDOW_SIZE_IN_SECONDS = 300.0
