#!/usr/bin/env python
#type: ignore
import itertools
import typing as t
import settings
from pathlib import Path
from pprint import pformat
import os
os.chdir(settings.BASE_DIR)
import click
from alembic.command import revision
from alembic.config import Config
from alembic.operations.ops import MigrationScript
configstr=str(Path(settings.BASE_DIR).joinpath('alembic.ini'))
config = Config(configstr)
def needupdate() -> t.List[tuple]:
    """Simulate the `alembic revision --autogenerate` command
    and return a list of generated operations.
    """


    revisions: t.List[MigrationScript] = []

    def process_revision_directives(context, revision, directives):
        nonlocal revisions
        revisions = list(directives)
        # Prevent actually generating a migration
        directives[:] = []

    revision(
        config=config,
        autogenerate=True,
        process_revision_directives=process_revision_directives,
    )

    arr=list(
        itertools.chain.from_iterable(
            op.as_diffs()
            for script in revisions
            for op in script.upgrade_ops_list
        )
    )
    return arr
from alembic import command
if arr:=needupdate():
    print(arr)
    command.revision(config=config,autogenerate=True)
    command.upgrade(config=config,revision='head')
    if os.getenv("MODE",'')=='STAGING':
        from devtools.hackapifox import main
        main.deleteall()
        main.generateall()
