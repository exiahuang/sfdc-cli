#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, argparse
from sfdc_cli.attachment import AttachmentApi

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.project:
            AttachmentApi(project_dir=args.project).download(
                args.savedir, limit=args.limit, filename=args.filename)
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
    subcommand.add_argument('-s',
                            '--savedir',
                            type=str,
                            help='save dir',
                            required=True)
    subcommand.add_argument('-l',
                            '--limit',
                            type=str,
                            default="100",
                            help='limit size, max 2000. default 100',
                            required=False)
    subcommand.add_argument(
        '--filename',
        type=str,
        default="{Id}_{Title}_v{VersionNumber}.{FileExtension}",
        help=
        'filename template, default {Id}_{Title}_v{VersionNumber}.{FileExtension}',
        required=False)
    subcommand.set_defaults(handler=handler)
