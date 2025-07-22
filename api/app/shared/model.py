from dataclasses import dataclass
from datetime import datetime as dt
from enum import Enum

from pydantic import BaseModel


class PaymentProcessorType(str, Enum):
    default = "default"
    fallback = "fallback"


class PaymentEntry(BaseModel):
    timestamp: dt
    amount: float
    processor: PaymentProcessorType
