APIPREFIX='/api/backend'
from .. import dependencies as praentdependencies
from fastapi import Depends
from typing import List,Callable,Any
import settings
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from common.globalFunctions import get_token
from common.CommonError import Common500Status,Common500OutShema,TokenException
from starlette.responses import JSONResponse
def check_admintoken(token: settings.UserTokenData = Depends(get_token))->Any:
    if not token.is_admin:
        out=jsonable_encoder(Common500OutShema(status=Common500Status.tokenerror,msg="not admin",data=""))
        print('1111')
        raise TokenException("not admin")

dependencies:List[Callable[...,Any]]=praentdependencies+[Depends(check_admintoken)]