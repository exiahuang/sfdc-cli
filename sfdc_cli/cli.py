#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from sfdc_cli.version import __version__, __desc__
from sfdc_cli.commands import register


def main():
    parser = argparse.ArgumentParser(description='%s v%s' %
                                     (__desc__, __version__))
    subparsers = parser.add_subparsers()
    register(parser, subparsers)

    # help
    def command_help(args):
        print(parser.parse_args([args.command, '--help']))

    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(handler=command_help)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
