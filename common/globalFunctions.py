import settings
from fastapi import Request
from jose import  jwt
from component.snowFlakeId import snowFlack

async def getorgeneratetoken(request)-> settings.UserTokenData:
    try:
        tokenstr = request.headers.get('token',None)
        if not tokenstr:
            tokenstr=request.cookies.get('token',None)

        if tokenstr:
            payload = jwt.decode(tokenstr, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            data = settings.UserTokenData.parse_obj(payload)
            return data
        else:
            raise Exception("has not token in header or cookie")
    except Exception as e:
        guest_token=settings.UserTokenData(id=snowFlack.getId(),is_guest=True)
        return guest_token

async def get_token(request:Request)->settings.UserTokenData:
    return request.state.token



