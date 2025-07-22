from datetime import UTC
from datetime import datetime as dt
from uuid import UUID

from fastapi import status
from httpx import Client, Response
from pydantic import BaseModel
from redis import Redis

from ..config import settings
from ..models.payments import ProcessPaymentRequest
from ..shared.model import PaymentEntry, PaymentProcessorType


class PaymentProcessorAPIRequest(BaseModel):
    correlationId: UUID
    amount: float
    requestedAt: dt


class PaymentProcessor:
    def __init__(self, http: Client, redis: Redis, request: ProcessPaymentRequest):
        self.http = http
        self.redis = redis
        self.request = request
        self.timestamp = dt.now(UTC)

    def _build_payload(self) -> str:
        return PaymentProcessorAPIRequest(
            correlationId=self.request.correlationId,
            amount=self.request.amount,
            requestedAt=self.timestamp,
        ).model_dump_json()

    def _store_payment(self, processor: PaymentProcessorType) -> None:
        entry = PaymentEntry(
            timestamp=self.timestamp,
            amount=self.request.amount,
            processor=processor,
        )
        score = entry.timestamp.timestamp()
        serialized = entry.model_dump_json()
        self.redis.zadd(settings.REDIS_PAYMENTS_KEY, {serialized: score})

    def _send_to_processor(self, url: str) -> Response | None:
        try:
            return self.http.post(
                url=f"{url}/payments",
                headers={"Content-Type": "application/json"},
                content=self._build_payload(),
            )
        except Exception:
            return None

    def process_payment(self) -> None:
        processors = [
            (PaymentProcessorType.default, settings.PAYMENT_PROCESSOR_DEFAULT_URL),
            (PaymentProcessorType.fallback, settings.PAYMENT_PROCESSOR_FALLBACK_URL),
        ]

        for processor_type, url in processors:
            response = self._send_to_processor(url)
            if response and response.status_code == status.HTTP_200_OK:
                self._store_payment(processor_type)
                return

        # If none succeeded, raise so the worker can re-queue
        raise RuntimeError("All payment processors failed")
