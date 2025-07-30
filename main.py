import asyncio
from glob import glob
from os.path import dirname, join, isfile, basename
from importlib import import_module

from fastapi import FastAPI

from settings import app_settings
from models import async_create

app = FastAPI(root_path='/api')

modules = glob(join(dirname(__file__), "endpoints/*.py"))
for file in modules:
    if isfile(file) and not file.endswith('__init__.py'):
        module = import_module('endpoints.%s' % basename(file)[:-3])
        app.include_router(getattr(module, "router"))

#asyncio.create_task(async_create())