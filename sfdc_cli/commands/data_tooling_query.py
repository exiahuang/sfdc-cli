#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.data import DataApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project:
            DataApi(project_dir=args.project).query_tooling(args.soql)
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name,
                                       help='see `%s -h`' % command_name)

    subcommand.add_argument('-p',
                            '--project',
                            type=str,
                            help='project dir, default is current working directory',
                            required=False,
                            default=".")
    subcommand.add_argument('-s',
                            '--soql',
                            type=str,
                            help='soql',
                            required=True)
    subcommand.set_defaults(handler=handler)
