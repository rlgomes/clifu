#!/usr/env python3
from distutils.core import setup

import os
import shutil

if not(os.path.exists("build")):
    os.mkdir("build")
    
shutil.copyfile('src/clifu.py', 'build/clifu')

setup (
    name='clf',
    version='0.1.0',
    author='Rodney Gomes',
    author_email='rodneygomes@gmail.com',
    url='',
    keywords = ['cli','commandlinefu'],
    scripts = ['build/clifu'],
    license='Apache 2.0 License',
    description='',
    long_description=open('README').read(),
)