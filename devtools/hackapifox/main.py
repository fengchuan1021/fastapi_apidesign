#type: ignore
import requests
import settings
from sqlalchemy import create_engine, MetaData
projectid=1231706
folderid=2071887

def createsession():
    session=requests.session()
    headers='''Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzgwMjYwLCJ0cyI6IjIwNDBmNDZiNDJlZDJmN2YiLCJpYXQiOjE2NTcxNjQ0NjQ1NjZ9.FWwxIPBVowh0Q6rfaC6D1Lg-sPmM81IBbnPpDekZlNk
Connection: keep-alive
Host: api.apifox.cn
Origin: https://www.apifox.cn
Referer: https://www.apifox.cn/
sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
X-Client-Mode: web
X-Client-Version: 2.1.29-alpha.1
X-Device-Id: jS6w1Gfc-dnQQ-AE9J-m4S1-q1juQK260ojt
X-Project-Id: 1210429'''
    headerarr=headers.split('\n')
    for item in headerarr:
        key,value=item.split(': ',1)
        #print(key,value)
        session.headers.update({key:value})
    session.headers.update({'X-Project-Id':str(projectid)})
    return session
import json
def addDataModel(name:str,jsonSchema,folderId:int=folderid):
    session=createsession()
    session.headers.update({'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'})
    ret=session.post(f'https://api.apifox.cn/api/v1/api-schemas?locale=zh-CN',data={'name':name,'folderId':folderId,'jsonSchema':json.dumps(jsonSchema)})
    print(ret.text)
def deleteDataModel(shemaid):
    session=createsession()
    ret=session.delete(f'https://api.apifox.cn/api/v1/api-schemas/{shemaid}?locale=zh-CN')
    print(ret.text)
def getDataModel():
    session=createsession()
    print("??/")

    ret=session.get(f'https://api.apifox.cn/api/v1/schemas-tree-list?locale=zh-CN').json()
    print(ret)
    return ret
import re
def gettableshema(name,info):
    dic={'type':"object"}
    properties={}
    requiredarr=[]
    for column in info.columns:
        item = {}
        if column.name in ['update_at','delete_at','is_deleted','create_at']:
            continue
        columntype=str(column.type)
        if columntype=='DATETIME':
            item['type']='string'
            item['format']='date-time'
        elif columntype=='BIGINT' or columntype=='INTEGER':
            item['type']='integer'
        elif columntype.startswith('VARCHAR'):
            item['type']='string'
            item['maxLength']=re.findall(r'(\d+)',columntype)[0]
        elif columntype=='Float':
            item['type']='number'
        elif columntype=='ENUM':
            item['type']="string"
            item["enum"]=column.type.enums
        if not column.primary_key:
            requiredarr.append(column.name)
        properties[column.name]=item
    dic["properties"]=properties
    dic["required"]=requiredarr
    return dic

def generateall():
    engine = create_engine(settings.DBURL.replace('mysql+aiomysql','mysql+pymysql'))
    metadata = MetaData(bind=engine)
    metadata.reflect()
    for tablename in metadata.tables:
        schemadict=gettableshema(tablename,metadata.tables[tablename])
        addDataModel('DB'+tablename,schemadict)

generateall()
#addDataModel("product",{"type":"object","properties":{"userID":{"type":"string"}},"x-apifox-orders":["userID"],"required":["userID"]})