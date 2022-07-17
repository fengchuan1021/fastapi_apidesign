from celery_app import celery_app
from pathlib import Path
import settings
import importlib,os
for f in Path(settings.BASE_DIR).joinpath('async_tasks').rglob('*.py'):
    if f.name.endswith('Task.py'):
        importlib.import_module(str(f.relative_to(settings.BASE_DIR)).replace(os.sep,'.')[0:-3])

