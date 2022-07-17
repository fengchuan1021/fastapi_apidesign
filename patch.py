#!/usr/bin/env python
import os

import site
files=site.getsitepackages()
targetdir=None
for f in files:
    if f.endswith('site-packages'):
        targetdir=f

files=os.listdir('patchs')
for filename in files:
    content=None
    with open(os.path.join('patchs',filename),'r',encoding='utf8') as f:
        filepath=f.readline().strip()

        content=f.read()
        realpath=filepath.replace('venv/Lib/site-packages',targetdir)
        print(f'{realpath=}')
        with open(realpath,'w',encoding='utf8') as tf:
            tf.write(content)