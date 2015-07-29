# -*- coding: utf-8 -*-
# (c) Lhassan Baazzi <baazzilhassan@gmail.com>

import os
from setuptools import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='scrapy-mongodb-queue',
    version='0.1.0',
    description='MongoDB-based components for Scrapy',
    long_description=LONG_DESC,
    author='Lhassan Baazzi',
    author_email='baazzilhassan@gmail.com',
    url='https://github.com/jbinfo/scrapy-mongodb',
    packages=['scrapy_mongodb_queue'],
    license='MIT',
    install_requires=['Scrapy==0.24.6', 'pymongo>=3.0']
)
