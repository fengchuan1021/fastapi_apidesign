#   timestamp: 2022-07-08T15:43:44+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseModel,validator,Field
from RegistryManager import Registry
class LoginplainInShema(BaseModel):
    username: str
    password: str


class Status(Enum):
    success = 'success'
    failed = 'failed'


class LoginplainOutShema(BaseModel):
    status: Status
    token: Optional[str] = None
    msg: Optional[str] = None


class RegisterInShema(BaseModel):
    username: str

    repassword:str= Field(..., exclude=True)
    password: str
    phone: str
    email: str
    def passwordcheck(cls, v,values): #type: ignore
        if 'repassword' in values and v != values['repassword']:
            raise ValueError('passwords do not match')
        elif 'repassword' in values and v == values['repassword']:
            return Registry.UserRegistry.get_password_hash(v)

class Status1(Enum):
    usernameexists = 'usernameexists'
    success = 'success'


class User(BaseModel):
    username: str
    phone: str
    email: str
    class Config:
        orm_mode = True

class RegisterOutShema(BaseModel):
    status: Status1
    user: User
