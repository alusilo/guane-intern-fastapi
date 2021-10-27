from celery import Celery
import redis
from config.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

redis_info = redis.Redis.from_url(CELERY_RESULT_BACKEND)

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


@celery.task
def move_to_next_stage(name, stage):
    redis_info.set(name, stage)
    return stage
