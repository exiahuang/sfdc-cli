#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.package_xml import PackageXml

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.dir and args.name:
            PackageXml(project_dir=args.project).buildFromServer(
                savepath=args.dir, filename=args.name)
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
                            '--dir',
                            type=str,
                            help='save directory',
                            required=False,
                            default=".")
    subcommand.add_argument('-n',
                            '--name',
                            type=str,
                            help='filename, default package.xml',
                            default="package.xml",
                            required=False)

    subcommand.set_defaults(handler=handler)
