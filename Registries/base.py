from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

import models
from models import Base
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI
from sqlalchemy.future import select
ModelType = TypeVar("ModelType", bound=Base)
from BroadcastManager import broadcastManager

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class

        """
        self.model = model

    async def findByPk(self,dbSession: AsyncSession,id: int) -> Optional[ModelType]:
        model= await dbSession.get(self.model,id)
        return model
        # stmt = select(self.model).options(selectinload(A.bs))
        # result = await dbSession.execute(stmt)
        # return result.scalars().first()
        # return dbSession.select(self.model).filter(self.model.id == id).first()



    async def create(self,dbSession: AsyncSession,shema_in:BaseModel) -> ModelType:

        db_model = self.model(**shema_in.dict())
        dbSession.add(db_model)

        return db_model


    def delete(self, model:ModelType)->None:
        model.is_deleted = True # type: ignore
    #def update(self,):