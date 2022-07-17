import importlib
from fastapi import FastAPI, File, UploadFile
import models

from fastapi import APIRouter,Depends
from common.dbsession import get_session
from typing import List
import json
from fastapi.openapi.utils import get_openapi
router=APIRouter(prefix='/apidesign')
from pydantic import BaseModel,constr
from sqlalchemy.ext.asyncio import AsyncSession
import os
import settings

from pathlib import Path
from enum import Enum
from typing import Any,Optional
from typing import Literal
from typing import Any
from devtools.generatefromopenapi import mymain
@router.post('/importapifox')
async def importfromapifox(file: UploadFile)->None:
    contents = await file.read()
    mymain(contents)
