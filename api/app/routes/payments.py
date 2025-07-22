from fastapi import APIRouter, Depends, status
from redis import Redis

from ..config import settings
from ..models.payments import ProcessPaymentRequest
from ..shared.dependency import get_redis

router = APIRouter(prefix="/payments")


@router.post(
    path="",
    status_code=status.HTTP_200_OK,
    summary="(Asynchronously) Process a payment request",
)
async def process_payment(
    request: ProcessPaymentRequest,
    redis: Redis = Depends(get_redis),
) -> None:
    redis.rpush(settings.REDIS_QUEUE, request.model_dump_json())

    return
