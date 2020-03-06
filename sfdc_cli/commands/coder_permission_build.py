#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from sfdc_cli.permission import Permission

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.sobject_dir:
            Permission(project_dir=args.project).build(
                sobject_meta_dir=args.sobject_dir,
                permission_save_path=args.savefile,
                include_all_sobject_permission=args.
                include_all_sobject_permission,
                field_list=args.fields)
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
    subcommand.add_argument('-f',
                            '--savefile',
                            type=str,
                            help='permission save file path',
                            required=True)
    subcommand.add_argument('--include_all_sobject_permission',
                            action='store_true',
                            help='include all sobject permission',
                            default=False,
                            required=False)
    subcommand.add_argument(
        '--fields',
        nargs="*",
        help='Sobject fields, if None, it will build all permission',
        default=None)
    subcommand.set_defaults(handler=handler)
