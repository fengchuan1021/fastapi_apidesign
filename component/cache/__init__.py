# from cache.cache import (
#     cache,
#     cache_one_day,
#     cache_one_hour,
#     cache_one_minute,
#     cache_one_month,
#     cache_one_week,
#     cache_one_year,
# )
#from cache.client import FastApiRedisCache
import json

from pydantic import BaseModel
from component.cache.key_builder import default_key_builder
from fastapi.encoders import jsonable_encoder
import asyncio
from functools import wraps
from typing import Callable, Optional, Type,Dict,Tuple
from inspect import signature, _empty
class CacheClass:
    def __init__(self):
        self._prefix = None
        self._expire = None
        self._init = False
        self. _key_builder = None
        self._enable = True
        self._loop = None
        self.redis=None
    def init(
        self,
        redis,
        prefix: str = "",
        expire: int = None,
        key_builder: Callable = default_key_builder,
        enable: bool = True,
    ):
        if self._init:
            return
        self._init = True
        self.redis = redis
        self._prefix = prefix
        self._expire = expire
        self._key_builder = key_builder
        self._enable = enable
        self._loop=asyncio.get_event_loop()

    def __call__(
            self,
            expire: int = None,
            key_builder: Callable = None,
            namespace: Optional[str] = "",
    ):
        """
        cache all function

        :param expire:
        :param key_builder:
        :param namespace:
        :return:
        """

        def wrapper(func):
            funcsig=signature(func)

            @wraps(func)
            async def inner(*args, **kwargs):
                nonlocal expire
                nonlocal key_builder
                expire = expire or self.get_expire()
                key_builder = key_builder or self.get_key_builder()

                key = key_builder(
                    funcsig, namespace, args=args, kwargs=kwargs
                )
                ret = await self.get(key)

                if ret is not None:
                    return json.loads(ret)
                if asyncio.iscoroutinefunction(func):
                    ret = await self._loop.run_until_complete(func(*args, **kwargs))
                    # await func(inDataType)
                else:
                    ret = func(*args, **kwargs)
                if(funcsig._return_annotation is not _empty) and issubclass(funcsig._return_annotation,BaseModel):
                    ret=jsonable_encoder(funcsig._return_annotation.parse_obj(ret))

                await self.set(key,ret, expire)
                return ret
                #
                # if request.method != "GET":
                #     return await func(request, *args, **kwargs)
                # if_none_match = request.headers.get("if-none-match")
                # if ret is not None:
                #     if response:
                #         response.headers["cache-Control"] = f"max-age={ttl}"
                #         etag = f"W/{hash(ret)}"
                #         if if_none_match == etag:
                #             response.status_code = 304
                #             return response
                #         response.headers["ETag"] = etag
                #     return coder.decode(ret)
                #
                # ret = await func(*args, **kwargs)
                # await backend.set(key, coder.encode(ret), expire)
                # return ret

            return inner

        return wrapper


    def get_prefix(self):
        return self._prefix

    def get_expire(self):
        return self._expire

    def get_coder(self):
        return self._coder

    def get_key_builder(self):
        return self._key_builder

    def get_enable(self):
        return self._enable
    
    async def clear(self, namespace: str = None, key: str = None) -> int:
        if namespace:
            lua = f"for i, name in ipairs(redis.call('KEYS', '{namespace}:*')) do redis.call('DEL', name); end"
            return await self.redis.eval(lua, numkeys=0)
        elif key:
            return await self.redis.delete(key)

    async def get_with_ttl(self, key: str) -> Tuple[int, str]:
        async with self.redis.pipeline(transaction=True) as pipe:
            return await (pipe.ttl(key).get(key).execute())


    async def get(self, key) -> str:
        return await self.redis.get(key)



    async def set(self, key: str, value: str, expire: int = None):
        return await self.redis.set(key, value, ex=expire)



cache=CacheClass()