# generated timestamp: 2022-07-08T15:43:44+00:00

from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, Header
from pydantic import BaseModel, Field, validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import models
import settings
from BroadcastManager import broadcastManager
from common.dbsession import get_session
from common.globalFunctions import get_token
from component.cache import cache
from RegistryManager import Registry

from .__init__ import APIPREFIX
from .UserShema import (
    LoginplainInShema,
    LoginplainOutShema,
    RegisterInShema,
    RegisterOutShema,
)

router = APIRouter(
    prefix=APIPREFIX,
)


# <editor-fold desc="login post: /loginplain">
@router.post('/loginplain', response_model=LoginplainOutShema)
async def login(
    body: LoginplainInShema,
    db: AsyncSession = Depends(get_session),
    token: settings.UserTokenData = Depends(get_token),
) -> LoginplainOutShema:
    """
    login
    """
    # if need current userinfo.but most time use token.id or token.username,token.phone.to reduce one database request
    # user=await Registry.UserRegistry.findByPk(token.id,db)

    pass


# </editor-fold>


# <editor-fold desc="register post: /register">
from .UserShema import Status1
from .UserShema import User as outUser
@router.post('/register', response_model=RegisterOutShema)
async def register(
    body: RegisterInShema,
    db: AsyncSession = Depends(get_session),
    token: settings.UserTokenData = Depends(get_token),
) -> RegisterOutShema:
    """
    register
    """
    # if need current userinfo.but most time use token.id or token.username,token.phone.to reduce one database request
    # user=await Registry.UserRegistry.findByPk(token.id,db)
    try:
        print('r??')
        UserModel=await Registry.UserRegistry.create(db,body)
        models.Role.create
        #await db.commit()
    except IntegrityError as e:
        return {'status':Status1.usernameexists,'msg':e._message()}

    return   {'status':Status1.success,'user':outUser.from_orm(UserModel)}
    pass


# </editor-fold>
