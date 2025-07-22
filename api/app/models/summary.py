from pydantic import BaseModel


class Summary(BaseModel):
    totalRequests: int
    totalAmount: float


class SummaryResponse(BaseModel):
    default: Summary
    fallback: Summary
