# import os
import argparse
import logging

_logger = logging.getLogger(__name__)


# def is_valid_file(parser, arg):
#     if not os.path.exists(arg):
#         parser.error("The file %s does not exist!" % arg)
#     else:
#         return open(arg, 'r')  # return an open file handle


def add_parser(subparsers: argparse.Action) -> None:
    parser = subparsers.add_parser('show')
    parser.add_argument('-i', '--input-file', required=True,
                        type=argparse.FileType(mode='rb', bufsize=4096))


def run(args: argparse.Namespace) -> None:
    _logger.debug("Loading image from file %r", args.input_file.name)
    pass
