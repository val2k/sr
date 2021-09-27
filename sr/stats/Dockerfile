FROM python:3.7

COPY . /stats
WORKDIR /stats

RUN useradd --user-group --create-home --no-log-init --shell /bin/bash celery
RUN pip install -r requirements.txt

ENTRYPOINT celery -A stats worker --loglevel=info --uid celery --gid celery
