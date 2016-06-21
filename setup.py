#!/usr/bin/env python

from distutils.core import setup

setup(
    name='blockheads',
    version='1.0',
    description='Basic Blockheads Client Library',
    author='wies',
    url='https://github.com/wiez/blockheads',
    packages=['blockheads'],
    requires=['requests', 'enet']
)
