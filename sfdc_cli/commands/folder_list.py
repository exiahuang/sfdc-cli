#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, argparse
from sfdc_cli.folder import FolderApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project:
            FolderApi(project_dir=args.project).list(args.name)
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
    subcommand.add_argument(
        '-n',
        '--name',
        type=str,
        help='metadata name, such as ReportFolder, EmailTemplate',
        required=True)
    subcommand.set_defaults(handler=handler)
