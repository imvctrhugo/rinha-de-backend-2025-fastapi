from contextlib import asynccontextmanager
from typing import AsyncGenerator

import httpx
from fastapi import FastAPI
from redis.asyncio import Redis

from .config import settings
from .routes.payments import router as payments_router
from .routes.summary import router as summary_router


@asynccontextmanager
async def custom_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.httpx_client = httpx.Client()
    app.state.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    yield

    await app.state.httpx_client.aclose()
    app.state.redis.close()


app = FastAPI(
    lifespan=custom_lifespan,
    title="Rinha de Backend 2025",
)

app.include_router(router=payments_router, tags=["Payments"])
app.include_router(router=summary_router, tags=["Summary"])
