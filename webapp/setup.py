#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup
from pathlib import Path

ROOT_PATH = Path(__file__).parent
README_PATH = ROOT_PATH / 'README.md'
REQUIREMENTS_PATH = ROOT_PATH / 'requirements.txt'
REQUIREMENTS_DEV_PATH = ROOT_PATH / 'requirements_dev.txt'

def stream_requirements(fd):
    """For a given requirements file descriptor, generate lines of
    distribution requirements, ignoring comments and chained requirement
    files.
    """
    for line in fd:
        cleaned = re.sub(r'#.*$', '', line).strip()
        if cleaned and not cleaned.startswith('-r'):
            yield cleaned


with REQUIREMENTS_PATH.open() as requirements_file:
    REQUIREMENTS = list(stream_requirements(requirements_file))


with REQUIREMENTS_DEV_PATH.open() as test_requirements_file:
    REQUIREMENTS_DEV = REQUIREMENTS[:]
    REQUIREMENTS_DEV.extend(stream_requirements(test_requirements_file))

setup(
    name='Matching Tool',
    version='0.0.0',
    description="Integrating HMIS and criminal justice data",
    long_description=README_PATH.read_text(),
    author="Center For Data Science and Public Policy",
    author_email='datascifellows@gmail.com',
    url='https://github.com/dssg/matching-tool',
    packages=[
        'backend',
        'backend.apis',
        'backend.validations'
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=REQUIREMENTS_DEV
)
