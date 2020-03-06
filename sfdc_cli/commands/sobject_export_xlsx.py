#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.sobject import SobjectApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project:
            SobjectApi(project_dir=args.project).export_xlsx(args.savepath)
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
                            '--savepath',
                            type=str,
                            help='save path',
                            required=True)
    subcommand.add_argument('--include_custom',
                            action='store_true',
                            help='include custom sobject',
                            default=True,
                            required=False)
    subcommand.add_argument('--include_standard',
                            action='store_true',
                            help='include standard sobject',
                            default=False,
                            required=False)
    subcommand.set_defaults(handler=handler)
