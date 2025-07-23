from typing import cast

from fastapi import Request
from httpx import Client as HttpxClient
from redis.asyncio import Redis


def get_http(request: Request) -> HttpxClient:
    return cast(HttpxClient, request.app.state.httpx_client)


def get_redis(request: Request) -> Redis:
    return cast(Redis, request.app.state.redis)
