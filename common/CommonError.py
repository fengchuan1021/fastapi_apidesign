from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, List,Any
from pydantic.generics import GenericModel



from enum import Enum

class Common500Status(Enum):
    validateerror = 'validateerror'
    neterror = 'neterror'
    dberror = 'dberror'
    tokenerror = 'tokenerror'


class Common500OutShema(BaseModel):
    status: Common500Status
    msg: Optional[str] = None
    data:Optional[Any]



