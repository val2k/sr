import logging

from celery import Celery, states

from src.constants import CELERY_NAME, CELERY_BROKER
from src.stat_service import StatService


logging.basicConfig()
logger = logging.getLogger("stats")
logger.setLevel(logging.INFO)

celery = Celery(CELERY_NAME, broker=CELERY_BROKER)
stat_service = StatService()

@celery.task(name='stats.ingestor')
def stats(stat_payload):
    # TODO(vkinyock): Better task status handling
    stat_service.insert_non_aggregated_stat(stat_payload)
    return states.SUCCESS

if __name__ == "__main__":
    StatService.aggregate_stats()
