#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, argparse
from sfdc_cli.tools import Tools

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        tools = Tools()
        if args.inline:
            tools.json_format(args.inline.read())
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name, help='json format')

    subcommand.add_argument('-i',
                            '--inline',
                            type=argparse.FileType('r', encoding='UTF-8'),
                            default=sys.stdin,
                            help='input json data')
    subcommand.set_defaults(handler=handler)
