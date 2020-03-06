#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sfdc-cli.
# https://github.com/exiahuang/sfdc-cli

# Licensed under the Apache License 2.0:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2020, exiahuang <exia.huang@outlook.com>

from sfdc_cli.version import __version__  # NOQA

import io, os, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if os.path.exists(".xyconfig/logging.conf"):
    import logging.config
    logging.config.fileConfig(".xyconfig/logging.conf")
else:
    import logging
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        format="[%(asctime)s][%(levelname)s] %(message)s")
