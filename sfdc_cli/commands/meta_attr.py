#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from sfdc_cli.metadata_api import MetadataApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.sourcepath:
            meta_api = MetadataApi(project_dir=args.project)
            meta_attr = meta_api.metadata_util.get_meta_attr(args.sourcepath)
            if meta_attr:
                print(json.dumps(meta_attr, indent=4))
            else:
                print("metadata attribute not found")
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name,
                                       help='see `%s -h`' % command_name)
    subcommand.add_argument('-p',
                            '--project',
                            type=str,
                            help='project dir',
                            required=False,
                            default=".")
    subcommand.add_argument('-s',
                            '--sourcepath',
                            type=str,
                            help='source path',
                            required=True)
    subcommand.set_defaults(handler=handler)