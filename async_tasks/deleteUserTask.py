import os
import settings
from sqlalchemy import text
from sqlalchemy import create_engine
engine = create_engine(settings.DBURL.replace('mysql+aiomysql','mysql+pymysql'))
print(settings.DBURL.replace('mysql+aiomysql','mysql+pymysql'))
def deletenewuser(userid):
    print('begintsk??')
    with engine.connect() as connection:
        print('what??')
        print(f"update user set is_deleted=1 where id={userid}")
        result = connection.execute(text(f"update user set is_deleted=1 where id={userid}"))