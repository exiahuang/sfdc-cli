#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.retrieve import RetrieveApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.dirs:
            retrieve_api = RetrieveApi(project_dir=args.project)
            retrieve_api.refresh(dirs=args.dirs)
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
    subcommand.add_argument('-d',
                            '--dirs',
                            nargs="*",
                            help='metadata directory name, example ./src/aura, ./src/classes, ./src/components, ./src/pages, ./src/triggers, etc ',
                            default=None)
    subcommand.set_defaults(handler=handler)
