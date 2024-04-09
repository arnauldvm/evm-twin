import argparse
import logging

_logger = logging.getLogger(__name__)


def add_parser(subparsers: argparse.Action) -> None:
    parser = subparsers.add_parser('show')
    parser.add_argument('-i', '--input-file', required=True,
                        type=argparse.FileType(mode='rb', bufsize=4096))


def run(args: argparse.Namespace) -> None:
    _logger.debug("Loading image from file %r", args.input_file.name)
    pass
