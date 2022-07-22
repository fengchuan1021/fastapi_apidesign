from typing import List
from pymysql.converters import escape_string #
def filterbuilder(filter:dict={})->str:
    arr:List[str]=[]
    if not filter:
        return ''

    oprationtable={'eq':'=','gt':'>','lt':'<','gte':'>=','lte':'<=','ne':'!='}
    for key in filter:
        value=filter[key]
        if not isinstance(value, int):
            value = f"'{escape_string(value)}'"
        #user.name__eq 'fengchuan'
        column,opration=key.split('__')
        if opration in oprationtable:
            arr.append(f"{column} {oprationtable[opration]} {value}")


    return ' and '.join(arr)
