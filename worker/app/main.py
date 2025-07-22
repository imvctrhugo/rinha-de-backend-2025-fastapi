# worker.py
import json
from concurrent.futures import ThreadPoolExecutor

from config import settings
from httpx import Client as HttpxClient
from loguru import logger
from models import ProcessPaymentRequest
from processor import PaymentProcessor
from redis import Redis

REDIS_QUEUE_NAME = settings.REDIS_QUEUE

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
http = HttpxClient()


def process_payment(payload: str):
    try:
        data = json.loads(payload)
        request = ProcessPaymentRequest(**data)

        logger.debug("Processing message.", request=request)

        processor = PaymentProcessor(
            http=http,
            redis=redis,
            request=request,
        )
        processor.process_payment()

    except RuntimeError:
        # Push it back to the queue if processors are unavailable
        logger.error(
            "Processors are unavailable, pushing message back to queue.",
            payload=payload,
        )
        redis.rpush(REDIS_QUEUE_NAME, payload)


def worker_loop():
    while True:
        item = redis.blpop(REDIS_QUEUE_NAME, timeout=1)
        if item:
            _, payload = item
            executor.submit(process_payment, payload)


if __name__ == "__main__":
    logger.info("Starting worker.")
    executor = ThreadPoolExecutor(max_workers=settings.WORKER_CONCURRENCY)
    worker_loop()
    logger.info("Worker finished or could not start.")
