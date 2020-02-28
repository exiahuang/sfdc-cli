#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import importlib

DIRNAME = os.path.dirname(os.path.abspath(__file__))


def register(parser, subparsers, **kwargs):
    for f in os.listdir(DIRNAME):
        if os.path.isfile(os.path.join(DIRNAME, f)) and f != "__init__.py":
            command = importlib.import_module("sfdc_cli.commands.%s" %
                                              f.replace(".py", ""))
            command.register(parser, subparsers, **kwargs)
