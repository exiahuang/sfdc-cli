#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.tools import Tools

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        tools = Tools()
        if args.from_dir and args.to_dir:
            tools.copy_lightning(args.from_dir, args.to_dir)
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name,
                                       help='see `%s -h`' % command_name)

    subcommand.add_argument('-f',
                            '--from_dir',
                            type=str,
                            help='from aura dir',
                            required=True)
    subcommand.add_argument('-t',
                            '--to_dir',
                            type=str,
                            help='to aura dir',
                            required=True)
    subcommand.set_defaults(handler=handler)
