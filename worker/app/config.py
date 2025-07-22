from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Payment Processor URLs
    PAYMENT_PROCESSOR_DEFAULT_URL: str = "http://payment-processor-default:8080"
    PAYMENT_PROCESSOR_FALLBACK_URL: str = "http://payment-processor-fallback:8080"

    REDIS_PAYMENTS_KEY: str = "processed_payments"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_QUEUE: str = "payment-process-requests"

    WORKER_CONCURRENCY: int = 10


settings = Settings()
