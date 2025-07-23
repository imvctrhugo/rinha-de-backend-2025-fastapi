from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis

from ..config import settings
from ..models.payments import ProcessPaymentRequest
from ..shared.dependency import get_redis

router = APIRouter()


@router.post(
    path="/payments",
    status_code=status.HTTP_202_ACCEPTED,
    summary="(Asynchronously) Process a payment request",
)
async def process_payment(
    request: ProcessPaymentRequest,
    redis: Redis = Depends(get_redis),
) -> None:
    await redis.rpush(settings.REDIS_QUEUE, request.model_dump_json())


@router.post(
    path="/purge-payments",
)
async def purge_payments(
    redis: Redis = Depends(get_redis),
) -> None:
    await redis.delete(settings.REDIS_PAYMENTS_KEY)
