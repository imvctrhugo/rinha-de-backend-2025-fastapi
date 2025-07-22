from datetime import datetime as dt
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class ProcessPaymentRequest(BaseModel):
    correlationId: UUID
    amount: float


class PaymentProcessorAPIRequest(BaseModel):
    correlationId: UUID
    amount: float
    requestedAt: dt


class PaymentProcessorType(str, Enum):
    default = "default"
    fallback = "fallback"


class PaymentEntry(BaseModel):
    timestamp: dt
    amount: float
    processor: PaymentProcessorType
