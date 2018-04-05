# coding: utf-8

import os

from matcher import __version__

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.readlines()

setup(
    name='matcher',
    version='0.0.1',
    description='CSH matcher',
    url='https://github.com/dssg/matching-tool',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)
