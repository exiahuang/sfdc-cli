#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from sfdc_cli.coder import Coder

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.soql:
            Coder(project_dir=args.project).insert_data_snippet_from_soql(
                args.soql)
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
