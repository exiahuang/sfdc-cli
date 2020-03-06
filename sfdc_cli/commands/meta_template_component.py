#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.metadata import Metadata

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.name:
            Metadata(args.project).new_component(args.name, args.overwrite)
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name,
                                       help='see `%s -h`' % command_name)

    subcommand.add_argument(
        '-p',
        '--project',
        type=str,
        help='project dir, default is current working directory',
        required=False,
        default=".")
    subcommand.add_argument('-n',
                            '--name',
                            type=str,
                            help='Api Name',
                            required=True)
    subcommand.add_argument('--overwrite',
                            action='store_true',
                            help='overwrite exist file',
                            required=False)
    subcommand.set_defaults(handler=handler)
