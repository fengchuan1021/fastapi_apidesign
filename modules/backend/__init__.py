APIPREFIX='/api/backend'
from .. import dependencies as praentdependencies
from fastapi import Depends
from typing import List,Callable,Any
import settings
from common.globalFunctions import get_token
def check_admintoken(token: settings.UserTokenData = Depends(get_token))->int:
    return token.is_admin
dependencies:List[Callable[...,Any]]=praentdependencies+[Depends(check_admintoken)]