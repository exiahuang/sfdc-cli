#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.package_xml import PackageXml

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.scandir and args.savedir and args.name and args.apiversion:

            PackageXml(project_dir=".").buildFromDir(
                scandir=args.scandir,
                savepath=args.savedir,
                filename=args.name,
                api_version=args.apiversion)
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name,
                                       help='see `%s -h`' % command_name)

    subcommand.add_argument('-s',
                            '--scandir',
                            type=str,
                            help='save directory',
                            required=False,
                            default="src")
    subcommand.add_argument('-d',
                            '--savedir',
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
    subcommand.add_argument('-v',
                            '--apiversion',
                            type=str,
                            help='api version, default 47.0',
                            default="47.0",
                            required=False)

    subcommand.set_defaults(handler=handler)
