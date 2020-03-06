#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, argparse, json
from sfdc_cli.rest_api import SfRestApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project and args.method and args.endpoint:
            if args.use_params:
                params = json.loads(args.params.read()) if args.params else None
            else:
                params = None
            SfRestApi(project_dir=args.project).call(method=args.method,
                                                     endpoint=args.endpoint,
                                                     params=params)
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
    subcommand.add_argument('-m',
                            '--method',
                            type=str,
                            help='method: GET/POST/PUT/DELETE. Default GET',
                            required=False,
                            default="GET")
    subcommand.add_argument(
        '-e',
        '--endpoint',
        type=str,
        help='endpoint, example: /services/data/v47.0/sobjects',
        required=True)
    subcommand.add_argument('--use_params',
                            action='store_true',
                            help='use params flag',
                            default=False)
    subcommand.add_argument('--params',
                            type=argparse.FileType('r', encoding='UTF-8'),
                            default=sys.stdin,
                            help='rest param')
    subcommand.set_defaults(handler=handler)
