import settings
import os
import re
from devtools import generateModel
def before_appstart()->None:

    generateModel.generate_model()

    resigtryTpl=open(os.path.join(settings.BASE_DIR, 'devtools','template', 'RegistryManager.py.tpl'), 'r', encoding='utf8').read()
    modelsContent=open(os.path.join(settings.BASE_DIR, 'models','allmodels.py.fromdb'), 'r', encoding='utf8').read()
    classnames=re.findall(r'class (.*?)\(Base\)',modelsContent)
    arr=[]
    for classname in classnames:
        if os.path.exists(os.path.join(settings.BASE_DIR, 'Registries', f'{classname}Registry.py')):
            arr.append(f'{classname}Registry : Registries.{classname}Registry\n')
        else:
            arr.append(f'{classname}Registry : CRUDBase[models.{classname}]\n')
    with open(os.path.join(settings.BASE_DIR, 'RegistryManager.py'), 'r', encoding='utf8') as f:
        oldcontent=f.read()

    newcontent=resigtryTpl.replace('{annotations}','    '.join(arr))
    if oldcontent!=newcontent:
        with open(os.path.join(settings.BASE_DIR, 'RegistryManager.py'), 'w', encoding='utf8') as f:
            f.write(newcontent)


    files=os.listdir(os.path.join(settings.BASE_DIR, 'Registries'))
    arr=[]
    for f2 in files:
        if f2.endswith('Registry.py'):
            name=f2.replace('.py','')
            arr.append(f"from .{name} import {name}")
    with open(os.path.join(settings.BASE_DIR, 'Registries', '__init__.py'), 'r', encoding='utf8') as f:
        oldcontent=f.read()
    newcontent='\n'.join(arr)
    if oldcontent!=newcontent:
        with open(os.path.join(settings.BASE_DIR, 'Registries', '__init__.py'), 'w', encoding='utf8') as f:
            f.write(newcontent)

    # files=os.listdir(os.path.join(settings.BASE_DIR,'listeners'))


    # for f in files:
    #     if f.endswith('.py') and f!='__init__.py':
    #
    #         content=open(os.path.join(settings.BASE_DIR,'listeners',f),'r',encoding='utf8').read()
    #
    #         if(tmps:=re.findall(r'createBroadcast\(.*?(\w+).*?,\s*(\w+)\)',content)):
    #
    #             for tmp in tmps:
    #                 imports.append(f"from listeners.{f[0:-3]} import {tmp[1]}")
    #                 lines.append(f"{tmp[0]}:Callable[['{tmp[1]}'],None]\n")
    # arr=[]
    # for classname in classnames:
    #     arr.append(f'{classname}Updated : Callable[[models.{classname},models.{classname},str],Any]\n')
    #     arr.append(f'{classname}Created : Callable[[models.{classname},str],Any]\n')
    #
    # content=open(os.path.join(settings.BASE_DIR, 'devtools','template', 'BroadcastManager.tpl'), 'r', encoding='utf8').read()
    # newcontent=content.replace('{annotations}','    '.join(arr))
    #
    # if os.path.exists(os.path.join(settings.BASE_DIR,  'BroadcastManager.py')):
    #     with open(os.path.join(settings.BASE_DIR,  'BroadcastManager.py'), 'r', encoding='utf8') as f:
    #         oldcontent=f.read()
    # else:
    #     oldcontent=''
    #
    # if oldcontent!=newcontent:
    #     with open(os.path.join(settings.BASE_DIR,  'BroadcastManager.py'), 'w', encoding='utf8') as f:
    #         f.write(newcontent)


