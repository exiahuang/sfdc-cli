#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sfdc-cli.
# https://github.com/exiahuang/sfdc-cli

# Licensed under the Apache License 2.0:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2020, exiahuang <exia.huang@outlook.com>

from setuptools import setup, find_packages
from sfdc_cli import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='sfdc-cli',
    version=__version__,
    description='sfdc development kit',
    long_description='''
sfdc development kit
''',
    keywords='sfdc-cli sdk tools xytools-cli salesforce',
    author='exiahuang',
    author_email='exia.huang@outlook.com',
    url='https://github.com/exiahuang/sfdc-cli',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        "requests[security]",
        "cryptography>=2.8",
        "XlsxWriter"
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'sfdc=sfdc_cli.cli:main',
        ],
    },
)
