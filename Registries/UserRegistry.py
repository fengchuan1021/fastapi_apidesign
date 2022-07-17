from Registries.base import CRUDBase
import models
from typing import Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
import settings
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy.sql import and_, or_
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi import Depends
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from sqlalchemy import select



class UserRegistry(CRUDBase[models.User]):


    async def getUserByPhoneOrUsername(self,db: AsyncSession,usernameOrPhone:str)->Optional[models.User]:
        query=select(self.model).filter(or_(models.User.username==usernameOrPhone,models.User.phone==usernameOrPhone))
        results = await db.execute(query)
        return results.scalar_one_or_none()

    def verify_password(self,plain_password:str, hashed_password : Optional[str])->bool:

        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self,password):# type: ignore
        return pwd_context.hash(password)

    async def authenticate(self,dbSession: AsyncSession, username: str, password: str)->bool | models.User:
        user = await self.getUserByPhoneOrUsername(dbSession,username)
        if not user:
            return False

        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self,data:models.User, expires_delta: Union[timedelta, None] = None)->str:
        to_encode = settings.UserTokenData.from_orm(data).dict()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt



