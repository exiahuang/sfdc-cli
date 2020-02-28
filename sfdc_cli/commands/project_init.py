#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.project import Project
command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def new_project(args):
        if args.projectdir:
            Project().init(project_dir=args.projectdir)
        else:
            print(parser.parse_args([command_name, '--help']))

    parser_project = subparsers.add_parser(command_name,
                                           help='see `%s -h`' % command_name)
    parser_project.add_argument('-d',
                                '--projectdir',
                                type=str,
                                help='project dir')
    parser_project.set_defaults(handler=new_project)
