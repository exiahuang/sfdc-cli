#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from sfdc_cli.coder import Coder

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.sobject:
            Coder(project_dir=args.project).soql_creater(
                objectApiName=args.sobject,
                is_custom_only=args.custom_field_only,
                is_updateable=args.updateable_field_only,
                include_relationship=args.include_relationship,
                include_comment=args.include_comment)

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
    subcommand.add_argument('--custom_field_only',
                            action='store_true',
                            help='only include custom field',
                            default=False,
                            required=False)
    subcommand.add_argument('--updateable_field_only',
                            action='store_true',
                            help='only include updateable field',
                            default=False,
                            required=False)
    subcommand.add_argument('--include_comment',
                            action='store_true',
                            help='include comment',
                            default=False,
                            required=False)
    subcommand.add_argument('--include_relationship',
                            action='store_true',
                            help='include relationship object',
                            default=False,
                            required=False)
    subcommand.set_defaults(handler=handler)
