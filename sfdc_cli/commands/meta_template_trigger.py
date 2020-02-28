#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sfdc_cli.metadata import Metadata

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.srcdir and args.name and args.sobject and args.template and args.apiversion:
            Metadata().new_trigger(args.name, args.sobject, args.template,
                                   args.srcdir, args.apiversion, args.overwrite)
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name,
                                       help='see `%s -h`' % command_name)

    subcommand.add_argument('-d',
                            '--srcdir',
                            type=str,
                            help='source dir',
                            required=True)
    subcommand.add_argument('-n',
                            '--name',
                            type=str,
                            help='Api Name',
                            required=True)
    subcommand.add_argument('-t',
                            '--template',
                            choices=[
                                "ApexTriggerAllEvents.trigger",
                                "ApexTriggerBulk.trigger",
                                "ApexTrigger.trigger",
                                "DomainTrigger.trigger",
                            ],
                            help='template name',
                            default="ApexTrigger.trigger",
                            required=False)
    subcommand.add_argument('--sobject',
                            type=str,
                            help='sobject name',
                            required=False)
    subcommand.add_argument('--overwrite',
                            action='store_true',
                            help='overwrite exist file',
                            required=False)
    subcommand.add_argument('-v',
                            '--apiversion',
                            type=str,
                            help='api version, default 47.0',
                            default="47.0",
                            required=True)
    subcommand.set_defaults(handler=handler)
