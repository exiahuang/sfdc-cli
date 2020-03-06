#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from sfdc_cli.coder import Coder

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.savedir:
            Coder(project_dir=args.project).create_sfdc_code(
                args.sobject,
                args.savedir,
                is_custom_only=args.custom_field_only,
                include_validate=args.include_validate)

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
                            '--sobject',
                            type=str,
                            help='sobject name',
                            required=True)
    subcommand.add_argument('-d',
                            '--savedir',
                            type=str,
                            help='save dir',
                            required=True)
    subcommand.add_argument('--custom_field_only',
                            action='store_true',
                            help='only include custom field',
                            default=False,
                            required=False)
    subcommand.add_argument('--include_validate',
                            action='store_true',
                            help='include field validator',
                            default=False,
                            required=False)
    subcommand.set_defaults(handler=handler)
