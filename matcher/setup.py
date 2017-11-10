# coding: utf-8

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.readlines()

setup(
    name='matcher',
    packages=['matcher', 'api'],
    include_package_data=True,
    install_requires=requirements
)
