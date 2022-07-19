APIPREFIX='/api/backend'
from .. import dependencies as praentdependencies
from fastapi import Depends
from typing import List,Callable,Any
import settings
#from fastapi.encoders import jsonable_encoder
from common.globalFunctions import get_token
from common.CommonError import TokenException

def check_admintoken(token: settings.UserTokenData = Depends(get_token))->None:
    if not token.is_admin:
        #out=jsonable_encoder(Common500OutShema(status=Common500Status.tokenerror,msg="not admin",data=""))
        raise TokenException("not admin")

dependencies:List[Callable[...,Any]]=praentdependencies+[Depends(check_admintoken)]