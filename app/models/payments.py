from uuid import UUID

from pydantic import BaseModel


class ProcessPaymentRequest(BaseModel):
    correlationId: UUID
    amount: float
