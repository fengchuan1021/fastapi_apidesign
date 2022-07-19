APIPREFIX='/api/backend/product'
from .. import dependencies as praentdependencies
from fastapi import Depends
from typing import List,Callable,Any
dependencies:List[Callable[...,Any]]=praentdependencies+[]