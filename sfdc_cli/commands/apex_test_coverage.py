#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.apex import ApexApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.filepath:
            ApexApi(project_dir=args.project).retrieve_apex_coverage(
                savefile=args.filepath)
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
    subcommand.add_argument('-f',
                            '--filepath',
                            type=str,
                            help='save filepath',
                            default="log/apex_coverage.log",
                            required=False)
    subcommand.set_defaults(handler=handler)
