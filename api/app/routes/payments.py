from fastapi import APIRouter, BackgroundTasks, Depends, status
from httpx import Client
from redis import Redis

from ..config import settings
from ..models.payments import ProcessPaymentRequest
from ..processors.payment import PaymentProcessor
from ..shared.dependency import get_http, get_redis

router = APIRouter(prefix="/payments")


# def queue_request(redis: Redis, request: ProcessPaymentRequest) -> None:
#     redis.rpush(settings.REDIS_QUEUE, request.model_dump_json())


@router.post(
    path="",
    status_code=status.HTTP_200_OK,
    summary="(Asynchronously) Process a payment request",
)
async def process_payment(
    request: ProcessPaymentRequest,
    # background_tasks: BackgroundTasks,
    # http: Client = Depends(get_http),
    redis: Redis = Depends(get_redis),
) -> None:
    # Payment process will run in the background after the response is sent.
    # background_tasks.add_task(queue_request, redis, request)
    redis.rpush(settings.REDIS_QUEUE, request.model_dump_json())

    return
