#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.retrieve import RetrieveApi
command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.dir and args.name:
            retrieve_api = RetrieveApi(project_dir=args.project)
            retrieve_api.retrieve(savedir=args.dir,
                                  zipfilename=args.name,
                                  metaTypes=args.metadata)
            if args.unzip:
                retrieve_api.unzip(os.path.join(args.dir, args.name),
                                   args.project, args.delete_after_unzip)
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
    subcommand.add_argument('-d',
                            '--dir',
                            type=str,
                            help='save dir',
                            required=True)
    subcommand.add_argument('-n',
                            '--name',
                            type=str,
                            help='project name, default package.zip',
                            default="package.zip")
    subcommand.add_argument('--unzip',
                            action='store_true',
                            help='unzip package.zip',
                            required=False)
    subcommand.add_argument('--delete_after_unzip',
                            action='store_true',
                            help='delete package.zip after unzip',
                            required=False)
    subcommand.add_argument('-m',
                            '--metadata',
                            nargs="*",
                            help='metadata list, default all metadata',
                            default=None)
    subcommand.set_defaults(handler=handler)
