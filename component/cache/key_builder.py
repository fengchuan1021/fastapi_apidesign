import hashlib
from typing import Optional

from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from settings import UserTokenData
ALWAYS_IGNORE_ARG_TYPES = [Request,AsyncSession,UserTokenData]
from inspect import Signature
def default_key_builder(
    funcsig:Signature,
    namespace: Optional[str] = "",
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
)->str:
    from component.cache import cache

    prefix = f"{cache.get_prefix()}:{namespace}:"
    cache_key = (
        prefix
        + hashlib.md5(  # nosec:B303
            f"{args}:{kwargs}".encode()
        ).hexdigest()
    )
    return cache_key