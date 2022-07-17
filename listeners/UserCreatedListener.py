import asyncio

import settings
from BroadcastManager import broadcastManager
import models
from common.globalFunctions import get_token
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.dbsession import get_session
from RegistryManager import Registry
import asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

@broadcastManager.BeforeModelCreated(models.User)
async def sendemail(usermodel:models.User,db: AsyncSession,token:settings.UserTokenData,reason=None):
    #set as admin default.
    usermodel.set_admin(True)


@broadcastManager.AfterModelCreated(models.User,background=True)
async def sendemail2(usermodel:models.User,db: AsyncSession,token:settings.UserTokenData):
    # insert some log
    #user2=models.User(username='testhook111',email='test@test.com',password='123456')
    #db.add(user2)
    #await db.commit()
    print('run in background')
    await asyncio.sleep(5)
    lg=models.Log(msg='usercreatd')
    db.add(lg)
    print('afterusercrat:',usermodel.username)