import json
from datetime import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, Query
from redis.asyncio import Redis

from ..config import settings
from ..models.summary import Summary, SummaryResponse
from ..shared.dependency import get_redis
from ..shared.model import PaymentEntry, PaymentProcessorType

router = APIRouter(prefix="/payments-summary")


async def fetch_payments(
    redis: Redis,
    from_: Optional[dt] = None,
    to: Optional[dt] = None,
) -> list[PaymentEntry]:
    min_score = from_.timestamp() if from_ else "-inf"
    max_score = to.timestamp() if to else "+inf"
    raw: list = await redis.zrangebyscore(
        name=settings.REDIS_PAYMENTS_KEY, min=min_score, max=max_score
    )
    return [PaymentEntry(**json.loads(entry)) for entry in raw]


@router.get(
    path="",
    response_model=SummaryResponse,
    summary="Return a summary of processed payments within an optional time range",
)
async def get_summary(
    from_: Optional[dt] = Query(default=None, alias="from"),
    to: Optional[dt] = Query(default=None),
    redis: Redis = Depends(get_redis),
) -> SummaryResponse:
    payments = await fetch_payments(redis, from_, to)

    totals = {
        PaymentProcessorType.default: {"count": 0, "amount": 0.0},
        PaymentProcessorType.fallback: {"count": 0, "amount": 0.0},
    }

    for p in payments:
        totals[p.processor]["count"] += 1
        totals[p.processor]["amount"] += p.amount

    return SummaryResponse(
        default=Summary(
            totalRequests=totals[PaymentProcessorType.default]["count"],
            totalAmount=round(totals[PaymentProcessorType.default]["amount"], 2),
        ),
        fallback=Summary(
            totalRequests=totals[PaymentProcessorType.fallback]["count"],
            totalAmount=round(totals[PaymentProcessorType.fallback]["amount"], 2),
        ),
    )
