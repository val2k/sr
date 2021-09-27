import json

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from celery import Celery, states
from pydantic import BaseModel

from src.constants import CELERY_BROKER, CELERY_NAME
from src.utils import add_timestamp_to_stat


app = FastAPI()
celery = Celery(CELERY_NAME, broker=CELERY_BROKER)

class Stat(BaseModel):
    token: str
    customer: str
    content: str
    timespan: int
    p2p: int
    cdn: int
    sessionDuration: int

@app.post("/stats")
async def stats(stat: Stat):
    jsonable_stat = jsonable_encoder(stat)
    jsonable_stat_with_timestamp = add_timestamp_to_stat(jsonable_stat)
    # TODO(vkinyock): Better task state handling.
    celery.send_task('stats.ingestor', args=[json.dumps(jsonable_stat_with_timestamp)])
    return states.SUCCESS
