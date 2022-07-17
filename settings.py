from pathlib import Path
from dotenv import load_dotenv
import os
BASE_DIR = Path(__file__).parent.__str__()
DEBUG=False
MODE=os.getenv("MODE","DEV")
if MODE=='DEV':
    DEBUG = True
    load_dotenv(os.path.join(BASE_DIR,'DEV.env'))

elif MODE=='STAGING':
    load_dotenv(os.path.join(BASE_DIR, 'STAGING.env'))
else:
    load_dotenv(os.path.join(BASE_DIR, 'PROD.env'))

REDISURL=os.getenv('REDISURL')
CELERY_RESULT_EXPIRED=3600

DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DATABASE=os.getenv('DATABASE')
DBURL='mysql+aiomysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)
print(f"{DBURL=}")
SECRET_KEY = "11a60e557ae59d6a4674bb5aeddcbc963bed0a4d44694f62c3be578d4155471d"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

from pydantic import BaseModel
from typing import Union
from UserRole import UserRole
class UserTokenData(BaseModel):
    id:int
    phone:str=''
    userrole=0
    username=''
    is_guest=False
    @property
    def is_admin(self)->int:
        if not self.userrole:
            self.userrole=0
        return self.userrole & UserRole.admin.value
    class Config:
        orm_mode = True
