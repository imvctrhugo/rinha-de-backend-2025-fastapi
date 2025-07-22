from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_PAYMENTS_KEY: str = "processed_payments"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_QUEUE: str = "payment-process-requests"


settings = Settings()
