# generated timestamp: 2022-07-19T01:39:31+00:00

from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI
from pydantic import BaseModel, Field, validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import settings
from common.dbsession import get_session
from common.globalFunctions import get_token
from component.cache import cache
from RegistryManager import Registry

from .__init__ import APIPREFIX, dependencies
from .productShema import AddproductInShema, AddproductOutShema

router = APIRouter(prefix=APIPREFIX, dependencies=dependencies)


# <editor-fold desc="addproduct post: /addproduct">
@router.post('/addproduct', response_model=AddproductOutShema)
async def addproduct(
    body: AddproductInShema,
    db: AsyncSession = Depends(get_session),
    token: settings.UserTokenData = Depends(get_token),
) -> AddproductOutShema | Dict:
    """
    addproduct
    """
    # if need current userinfo.but most time use token.id or token.username,token.phone.to reduce one database request
    # user=await Registry.UserRegistry.findByPk(db,token.id)

    pass


# </editor-fold>
