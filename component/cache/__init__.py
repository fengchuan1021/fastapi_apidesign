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
import asyncio
from pydantic import BaseModel
from redis.asyncio import Redis
import settings
from component.cache.key_builder import default_key_builder
from fastapi.encoders import jsonable_encoder
import asyncio
from functools import wraps
from typing import Callable, Optional, Type,Dict,Tuple,Any,TypeVar,Callable,overload,cast
from inspect import signature, _empty
F = TypeVar('F', bound=Callable[..., Any])
_StrType = TypeVar("_StrType", bound=str | bytes)

class CacheClass:
    #self._loop: asyncio.AbstractEventLoop
    def __init__(self)->None:
        self._prefix:str = ''
        self._expire:int = 0
        self._init:bool = False
        self. _key_builder:Callable[...,Any]
        self._enable:bool = True
        self._loop:asyncio.AbstractEventLoop
        self.redis:Redis
    def init(
        self,
        redis:Redis,
        prefix: str = "",
        expire: int = None,
        key_builder: Callable = default_key_builder,
        enable: bool = True,
    )->None:#type: ignore
        if self._init:
            return
        self._init = True
        self.redis = redis
        self._prefix = prefix
        self._expire = expire if expire else settings.DEFAULT_REDIS_EXPIRED
        self._key_builder = key_builder
        self._enable = enable
        self._loop=asyncio.get_event_loop()

    @overload
    def __call__(self,__func: F) -> F: ...

    @overload
    def __call__(self,*, expire: int,key_builder: F=None,namespace:str='') -> Callable[[F], F]: ...

    def __call__(
            self,
            __func:F=None,
            *,
            expire: int = 0,
            key_builder: Callable[...,Any] = None,
            namespace: str = "",
    )->Any:
        """
        cache all function

        :param expire:
        :param key_builder:
        :param namespace:
        :return:
        """

        def decorator(func:F)->F:
            funcsig=signature(func)

            @wraps(func)
            async def inner(*args:Any, **kwargs:Any)->Any:
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
                #funcsig._return_annotation.__args__[0].parse_obj()
                if(funcsig.return_annotation is not _empty) and issubclass(funcsig.return_annotation,BaseModel):
                    ret=jsonable_encoder(funcsig.return_annotation.parse_obj(ret))

                await self.set(key,ret, expire)
                return ret
            return cast(F, inner)

        if __func is not None:
            return decorator(__func)
        else:
            return decorator



    def get_prefix(self)->str:
        return self._prefix

    def get_expire(self)->int:
        return self._expire



    def get_key_builder(self)->Callable[...,Any]:
        return self._key_builder

    def get_enable(self)->bool:
        return self._enable
    
    async def clear(self, namespace: str = None, key: str = None) -> int:
        if namespace:
            lua = f"for i, name in ipairs(redis.call('KEYS', '{namespace}:*')) do redis.call('DEL', name); end"
            return await self.redis.eval(lua, numkeys=0)
        elif key:
            return await self.redis.delete(key)
        else:
            return 0

    async def get_with_ttl(self, key: str) -> Tuple[int, str]:
        async with self.redis.pipeline(transaction=True) as pipe:
            return await (pipe.ttl(key).get(key).execute()) #type: ignore


    async def get(self, key:str) -> _StrType | None:
        return await self.redis.get(key)



    async def set(self, key: str, value: str, expire: int = None)-> bool | None:
        return await self.redis.set(key, value, ex=expire)



cache=CacheClass()