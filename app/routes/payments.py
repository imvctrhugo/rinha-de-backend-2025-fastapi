from fastapi import APIRouter, BackgroundTasks, Depends, status
from httpx import Client
from redis import Redis

from ..models.payments import ProcessPaymentRequest
from ..processors.payment import PaymentProcessor
from ..shared.dependency import get_http, get_redis

router = APIRouter(prefix="/payments")


@router.post(
    path="",
    status_code=status.HTTP_200_OK,
    summary="(Asynchronously) Process a payment request",
)
async def process_payment(
    request: ProcessPaymentRequest,
    background_tasks: BackgroundTasks,
    http: Client = Depends(get_http),
    redis: Redis = Depends(get_redis),
) -> None:
    # Payment process will run in the background after the response is sent.
    payment_processor = PaymentProcessor(http=http, redis=redis, request=request)
    background_tasks.add_task(payment_processor.process_payment)

    return
