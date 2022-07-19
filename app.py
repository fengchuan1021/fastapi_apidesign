import fastapi.exceptions
import settings
import asyncio
import os
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTasks
from sqlalchemy.exc import IntegrityError
from RegistryManager import Registry
import importlib
from typing import Any
from fastapi import FastAPI,Request
import redis.asyncio as redis
from component.cache import cache
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from common.CommonError import Common500OutShema,Common500Status,TokenException
from sqlalchemy.exc import OperationalError
from common.globalFunctions import getorgeneratetoken
from datetime import timedelta
from BroadcastManager import broadcastManager
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
if os.name!='nt':
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


app = FastAPI(redoc_url=None,docs_url=None,openapi_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def finalcommit(session: AsyncSession)->None:
    try:
        await session.commit()
        await session.close()
    except Exception as e:
        pass

@app.middleware("http")
async def validate_tokenandperformevent(request: Request, call_next:Any)->Response:

    request.state.token=await getorgeneratetoken(request)
    try:
        response = await call_next(request)  # This request will be modified and sent
        if dbsession:=request.state._state.get('db_client',None):
            await dbsession.commit()
            if (updatearr:=set(dbsession._updateArr)) or (createdarr:=set(dbsession._createdArr)):# type: ignore
                backgroundtasks=BackgroundTasks()
                if updatearr:
                    backgroundtasks.add_task(broadcastManager.fireAfterUpdated,updatearr,dbsession,request.state.token,background=True)# type: ignore
                if createdarr:
                    backgroundtasks.add_task(broadcastManager.fireAfterCreated,createdarr,dbsession,request.state.token,background=True)# type: ignore
                backgroundtasks.add_task(finalcommit,dbsession)
                response.background =backgroundtasks
    except OperationalError as e:
        jsonout = jsonable_encoder(Common500OutShema(status=Common500Status.dberror,msg=str(e)))
        response=JSONResponse(jsonout,status_code=500)
        try:
            await request.state.db_client.close()
        except:
            pass
    except IntegrityError as e:
        jsonout = jsonable_encoder(Common500OutShema(status=Common500Status.dberror, msg="Duplicate entry"))
        response=JSONResponse(jsonout,status_code=500)
        try:
            await request.state.db_client.close()
        except:
            pass
    except TokenException as e:
        jsonout = jsonable_encoder(Common500OutShema(status=Common500Status.tokenerror, msg=str(e)))
        response=JSONResponse(jsonout,status_code=500)
    except fastapi.exceptions.ValidationError as e:
        jsonout = jsonable_encoder(Common500OutShema(status=Common500Status.validateerror,msg='',data=e.errors()))
        response=JSONResponse(jsonout,status_code=500)
    if request.state.token.is_guest:
        response.set_cookie('token',Registry.UserRegistry.create_access_token(request.state.token),timedelta(seconds=3600*24*30))
    return response

@app.on_event("startup")
async def startup()->None:
    pool = redis.ConnectionPool.from_url(url=settings.REDISURL)
    r:redis.Redis = redis.Redis(connection_pool=pool)
    cache.init(r, prefix="xt-cache",expire=3600)


for f in Path(settings.BASE_DIR).joinpath('modules').rglob('*.py'):
    if f.name.endswith('Controller.py'):
        controller = importlib.import_module(
            str(f.relative_to(settings.BASE_DIR)).replace(os.sep,'.')[0:-3]
        )

        app.include_router(controller.router)


for f in Path(settings.BASE_DIR).joinpath('listeners').rglob('*.py'):
    if f.name.endswith('Listener.py'):
        importlib.import_module(str(f.relative_to(settings.BASE_DIR)).replace(os.sep,'.')[0:-3])


if __name__ == "__main__":
    if settings.MODE == 'DEV':
        from devtools import debugtools
        from devtools.apidesign import router
        import multiprocessing
        app.include_router(router)
        from fastapi.staticfiles import StaticFiles
        app.mount("/apidesign/importfromapifox", StaticFiles(directory="devtools/uploadpage", html=True),
                  name="uploadfromapifox")
        backgroundprocess = multiprocessing.Process(target=debugtools.before_appstart)
        backgroundprocess.start()


    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info",reload=settings.DEBUG)