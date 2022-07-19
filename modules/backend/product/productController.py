# generated timestamp: 2022-07-19T01:35:20+00:00

from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI
from pydantic import BaseModel, Field, validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from BroadcastManager import broadcastManager
from common.dbsession import get_session
from common.globalFunctions import get_token
from component.cache import cache
from RegistryManager import Registry

from .__init__ import APIPREFIX, dependencies
from .productShema import AddproductPostRequest, AddproductPostResponse

router = APIRouter(prefix=APIPREFIX, dependencies=dependencies)


# <editor-fold desc="addproduct post: /addproduct">
@router.post('/addproduct', response_model=AddproductPostResponse)
async def addproduct(
    body: AddproductPostRequest,
    db: AsyncSession = Depends(get_session),
    token: settings.UserTokenData = Depends(get_token),
) -> AddproductPostResponse | Dict:
    """
    addproduct
    """
    # if need current userinfo.but most time use token.id or token.username,token.phone.to reduce one database request
    # user=await Registry.UserRegistry.findByPk(db,token.id)

    pass


# </editor-fold>
