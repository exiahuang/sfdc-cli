#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from sfdc_cli.permission import Permission

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.sobject_dir and args.type:
            if args.type == "fields":
                Permission(project_dir=args.project).list_fields(
                    sobject_meta_dir=args.sobject_dir)
            elif args.type == "sobject":
                Permission(project_dir=args.project).list_sobjects(
                    sobject_meta_dir=args.sobject_dir)
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
                            '--sobject_dir',
                            type=str,
                            help='sobject metadata dir',
                            required=True)
    subcommand.add_argument('-t',
                            '--type',
                            type=str,
                            help='list type',
                            required=True)
    subcommand.set_defaults(handler=handler)
