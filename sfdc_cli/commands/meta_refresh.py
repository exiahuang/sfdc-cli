#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.metadata_api import MetadataApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.sourcepath:
            meta_api = MetadataApi(project_dir=args.project)
            if meta_api._check_is_aura_dir(args.sourcepath):
                meta_api.refresh_aura(aura_dir=args.sourcepath)
            else:
                meta_api.refresh_metadata(filepath=args.sourcepath)
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
                            help='source path or directory',
                            required=True)
    subcommand.set_defaults(handler=handler)
