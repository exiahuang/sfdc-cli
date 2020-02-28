#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sfdc-cli.
# https://github.com/exiahuang/sfdc-cli

# Licensed under the Apache License 2.0:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2020, exiahuang <exia.huang@outlook.com>

from preggy import expect

from sfdc_cli import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):

    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
