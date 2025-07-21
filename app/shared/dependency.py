from typing import cast
from fastapi import Request
from redis import Redis


def get_redis(request: Request) -> Redis:
    return cast(Redis, request.app.state.redis)
