#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.testclass import Testclass

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.sourcepath:
            Testclass(project_dir=args.project).run(args.sourcepath)
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
