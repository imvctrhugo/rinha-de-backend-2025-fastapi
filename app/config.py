from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Payment Processor URLs
    PAYMENT_PROCESSOR_DEFAULT_URL: str = "http://payment-processor-default:8080"
    PAYMENT_PROCESSOR_FALLBACK_URL: str = "http://payment-processor-fallback:8080"

    REDIS_PAYMENTS_KEY: str = "processed_payments"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


settings = Settings()
