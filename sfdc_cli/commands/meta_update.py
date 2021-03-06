#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.metadata_api import MetadataApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.sourcepath:
            meta_api = MetadataApi(project_dir=args.project)
            meta_api.update_metadata(args.sourcepath, args.force)
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
                            '--sourcepath',
                            type=str,
                            help='source path',
                            required=True)
    subcommand.add_argument('--force',
                            action='store_true',
                            help='force update, overwrite server',
                            required=False)
    subcommand.set_defaults(handler=handler)
