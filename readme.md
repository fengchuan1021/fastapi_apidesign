### install and patch

install requirements:

```
pip install -r requirements.txt
```

######     windows error

​    some library do not support windows. so you can open requirements.txt remove uvloop==0.16.0



patch thirdparty library.

```
python patch.py
```

set up git hook.

```
git config --local core.hooksPath .githooks/
```



### start up server

```
python app.py
```

or

```
python -m uvicorn app:app --reload
```

### start celery worker(linux only)

```
celery -A celery_mainworker worker -l info
```



### two methods generate cotroller and shema from openapi.json:

1. generate controller from cli.

```shell
./devtools/generatefromopenapi.py d:\myxt\openapi.json
```

2. visit http://127.0.0.1:8000/apidesign/importfromapifox   drag json file in the upload box



alembic revision --autogenerate -m "add root_cause table"
alembic upgrade head