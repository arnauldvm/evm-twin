import argparse
import logging

import numpy
import cv2 as cv

_logger = logging.getLogger(__name__)

# Adapted from https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html


def add_parser(subparsers: argparse.Action) -> None:
    parser = subparsers.add_parser('show')
    parser.add_argument('-i', '--input-file', required=True,
                        type=argparse.FileType(mode='rb', bufsize=4096))


def run(args: argparse.Namespace) -> None:
    _logger.debug("Loading image from file %r", args.input_file.name)
    # img = cv.imread(args.input_file.name)
    #   this re-opens the file, and cannot read from stdin
    try:
        image_bytes = numpy.asarray(bytearray(args.input_file.read()), dtype=numpy.uint8)
        img = cv.imdecode(image_bytes, cv.IMREAD_UNCHANGED)
    finally:
        args.input_file.close()
    if img is None:
        raise Exception("Could not read the image.")

    _logger.debug("Displaying image")
    cv.imshow("Display window", img)
    _ = cv.waitKey(0)
