#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.project import Project
command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def new_project(args):
        if args.projectdir:
            Project().init(project_dir=args.projectdir,
                           username=args.username,
                           password=args.password,
                           security_token=args.security_token,
                           sourcedir=args.sourcedir,
                           api_version=args.api_version,
                           is_sandbox=args.sandbox)
        else:
            print(parser.parse_args([command_name, '--help']))

    parser_project = subparsers.add_parser(command_name,
                                           help='see `%s -h`' % command_name)
    parser_project.add_argument('-d',
                                '--projectdir',
                                type=str,
                                help='project dir')
    parser_project.add_argument('-u',
                                '--username',
                                type=str,
                                help='username',
                                default="none")
    parser_project.add_argument('-t',
                                '--security_token',
                                type=str,
                                help='security token, default blank.',
                                default="")
    parser_project.add_argument('-p',
                                '--password',
                                type=str,
                                help='password',
                                default="none")
    parser_project.add_argument('-s',
                                '--sourcedir',
                                type=str,
                                help='source directory, default src',
                                default="src")
    parser_project.add_argument('-v',
                                '--api_version',
                                type=float,
                                help='api version, default 47.0',
                                default=47.0)
    parser_project.add_argument('--sandbox',
                                action='store_true',
                                help='is sandbox',
                                default=False)
    parser_project.set_defaults(handler=new_project)
