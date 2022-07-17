import settings
from BroadcastManager import broadcastManager
import models
from common.globalFunctions import get_token
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.dbsession import get_session
from RegistryManager import Registry


@broadcastManager.BeforeModelCreated(models.Order)
async def setInventorytoreserved(ordermodel:models.Order,db: AsyncSession,token:settings.UserTokenData,reason=''):

    if not token.is_admin:
        Registry.InventoryManager.reserveforuserOrder(ordermodel)



@broadcastManager.BeforeModelCreated(models.Order)
async def setEmailtoUserForConfirm(ordermodel:models.Order,db: AsyncSession,token:settings.UserTokenData,reason=''):

    if not token.is_admin:
        pass
