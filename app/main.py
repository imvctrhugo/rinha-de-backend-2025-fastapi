from contextlib import asynccontextmanager
from typing import AsyncGenerator
from redis import Redis

from fastapi import FastAPI

from .routes.payments import router as payments_router
from .config import settings


@asynccontextmanager
async def custom_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    yield
    app.state.redis.close()


app = FastAPI(
    lifespan=custom_lifespan,
    title="Rinha de Backend 2025",
)

app.include_router(router=payments_router, tags=["Analyze"])
