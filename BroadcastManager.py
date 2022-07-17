
from typing import Type,TypeVar,List
import asyncio

import settings
from models import Base
from pydantic import  BaseModel
INDATATYPE=Type[BaseModel]
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict,Callable,Any,Generic,cast
Model= TypeVar("Model", bound=Base)
F = TypeVar('F', bound=Callable[..., Any])
class BroadcastManager():

    def __init__(self)->None:
        self.broadcastqueue={} #type: ignore

    def AfterModelUpdated(self,listenModel : Type[Model],background:bool=False)->Callable[[F], F]:
        queuename = f'After{listenModel.__name__}Updated{background}'
        if queuename not in self.broadcastqueue:
            self.broadcastqueue[queuename] = []

        def decorator(func:F)->F:
            self.broadcastqueue[queuename].append(func)
            def wrapper(*args:Any,**kwargs:Any)->Any:
               return func(*args,**kwargs)

            return cast(F, wrapper)
        return decorator

    async def fireAfterUpdated(self,updatedmodels:List[Model],db: AsyncSession,token:settings.UserTokenData,background:bool=False)->None:
        for model in updatedmodels:
            name=f'After{model.__class__.__name__}Updated{background}'
            if name in self.broadcastqueue:
                for func in self.broadcastqueue[name]:
                    if asyncio.iscoroutinefunction(func):
                        await func(model,db,token)
                    else:
                        raise Exception("call back must be a async function")

    def BeforeModelCreated(self,listenModel : Type[Model])->Callable[[F], F]:
        queuename=f'Before{listenModel.__name__}Created'
        if queuename not in self.broadcastqueue:
            self.broadcastqueue[queuename] = []
        def decorator(func:F)->F:
            self.broadcastqueue[queuename].append(func)
            def wrapper(*args:Any,**kwargs:Any)->Any:
                return func(*args,**kwargs)
            return cast(F, wrapper)
        return decorator
    async def fireBeforeCreated(self,newmodels:List[Model],db: AsyncSession,token:settings.UserTokenData)->None:
        # no meaning to run listener in background. because created model could be rollback. but background task dont know.
        for model in newmodels:
            name=f'Before{model.__class__.__name__}Created'
            if name in self.broadcastqueue:
                for func in self.broadcastqueue[name]:
                    if asyncio.iscoroutinefunction(func):
                        await func(model,db,token)
                    else:
                        raise Exception("call back must be a async function")

    def AfterModelCreated(self,listenModel : Type[Model],background:bool=False)->Callable[[F], F]:
        queuename = f'After{listenModel.__name__}Created{background}'
        if queuename not in self.broadcastqueue:
            self.broadcastqueue[queuename] = []
        def decorator(func:F)->F:
            self.broadcastqueue[queuename].append(func)
            def wrapper(*args:Any,**kwargs:Any)->Any:
               return func(*args,**kwargs)
            return cast(F, wrapper)
        return decorator

    async def fireAfterCreated(self,newmodels:List[Model],db: AsyncSession,token:settings.UserTokenData,background:bool=False)->None:
        for model in newmodels:
            name=f'After{model.__class__.__name__}Created{background}'
            if name in self.broadcastqueue:
                for func in self.broadcastqueue[name]:
                    if asyncio.iscoroutinefunction(func):
                        await func(model,db,token)
                    else:
                        raise Exception("call back must be a async function")

broadcastManager=BroadcastManager()
