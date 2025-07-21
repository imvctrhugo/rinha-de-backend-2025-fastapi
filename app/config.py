from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    QUEUE_NAME: str = "payment-process-requests"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


settings = Settings()
