from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union,Tuple
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from models import Base
from sqlalchemy.future import select
from sqlalchemy import text, func
from common.filterbuilder import filterbuilder
ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def findByPk(self,dbSession: AsyncSession,id: int) -> Optional[ModelType]:
        results=await dbSession.execute(select(self.model).where(self.model.id==id,self.model.is_deleted==0))
        return results.scalar_one_or_none()

    async def create(self,dbSession: AsyncSession,shema_in:BaseModel) -> ModelType:
        db_model = self.model(**shema_in.dict())
        dbSession.add(db_model)
        return db_model

    async def getList(self,dbSession: AsyncSession,pageNum:int=1,pageSize:int=20,filter:dict={},order_by:str='',calcTotalNum:bool=False)->Tuple[List[ModelType],int]:

        if calcTotalNum:
            totalstatment=select(func.count('*')).select_from(self.model).where(text(filterbuilder(filter)))
            result=await dbSession.execute(totalstatment)
            totalNum=result.scalar_one()
        else:
            totalNum = 0

        stament=select(self.model).where(text(filterbuilder(filter))).limit(pageSize).offset((pageNum-1)*pageSize).order_by(text(order_by))
        results=await dbSession.execute(stament)
        return results.scalars().all(),totalNum



    def delete(self, model:ModelType)->None:
        model.is_deleted = True

