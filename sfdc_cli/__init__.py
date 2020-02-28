#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sfdc-cli.
# https://github.com/exiahuang/sfdc-cli

# Licensed under the Apache License 2.0:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2020, exiahuang <exia.huang@outlook.com>

from sfdc_cli.version import __version__  # NOQA
import urllib3
urllib3.disable_warnings()

import logging
# todo
#  %(asctime)s %(levelname)s \t: %(message)s
logging.basicConfig(
    level=logging.INFO,
    format=
    "[ %(filename)s :%(lineno)s - %(funcName)20s() %(levelname)s ] %(message)s")
