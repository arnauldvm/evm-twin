import argparse
import logging

import numpy
import cv2 as cv

_logger = logging.getLogger(__name__)

# Adapted from https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html


def add_parser(subparsers: argparse.Action) -> None:
    description = "Read video from file or camera and display n-th frame in popup"
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'capture', description=description, help=description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input-file',
                       type=argparse.FileType(mode='rb', bufsize=4096),
                       help="Path of file from which to read the video")
    group.add_argument('-c', '--camera', action='store_true')
    parser.add_argument('-n', '--image-num', required=True, type=int,
                        help="Index of the frame to display")


def run(args: argparse.Namespace) -> None:
    if args.camera:
        _logger.debug("Capturing image from default camera")
        video = cv.VideoCapture(0)
    else:
        _logger.debug("Capturing image from video file %r", args.input_file.name)
        video = cv.VideoCapture(args.input_file.name)
    if not video.isOpened():
        raise Exception("Could not read the video.")
    #   this re-opens the file, and cannot read from stdin

    # Attempt at reading video from bytes (does not work):
    # try:
    #     video_array = numpy.frombuffer(args.input_file.read(), dtype=numpy.uint8)
    #     video = cv.imdecode(video_array, cv.IMREAD_COLOR)
    # finally:
    #     args.input_file.close()
    # if video is None:
    #     raise Exception("Could not read the video.")
    # count = 0
    # for frame in video:
    #     count += 1
    #     if count == args.image_num:
    #         break
    #     _logger.debug("Ignoeing frame %r", count)

    count = 0
    while True:
        status, frame = video.read()
        if not status:
            _logger.warn("Video stream interrupted")
            break
        count += 1
        if count == args.image_num:
            break
        _logger.debug("Ignoring frame %r", count)

    _logger.debug("Displaying frame")
    cv.imshow("Display window", frame)
    _ = cv.waitKey(0)
