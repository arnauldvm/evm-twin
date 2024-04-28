import argparse
import logging
from dataclasses import dataclass

import numpy
import cv2 as cv
from dlib import rectangle, rgb_pixel, point
import face_recognition as fr

_logger = logging.getLogger(__name__)

# FACES_DETECTION_UPSAMPLES: int = 1
FACES_DETECTION_UPSAMPLES: int = 3
FACES_DETECTION_MODEL: str = 'hog'
# FACES_DETECTION_MODEL: str = 'cnn'

# FACES_ENCODINGS_JITTERS = 1
FACES_ENCODINGS_JITTERS = 3

FONT_FACE = cv.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_THICKNESS = 2
(FONT_HEIGHT, FONT_WIDTH) = cv.getTextSize(text='0', fontFace=FONT_FACE, fontScale=FONT_SCALE,
                                            thickness=FONT_THICKNESS+2)[0]

BOX_COLOR: rgb_pixel = rgb_pixel(255, 128, 64)  # BRG
BOX_COLOR_HIGHLIGHT: rgb_pixel = rgb_pixel(0, 0, 255)  # BRG
BOX_THICKNESS: int = 2
MAX_DISPLAY_WIDTH: int = 1536
MAX_DISPLAY_HEIGHT: int = 1024


def add_parser(subparsers: argparse.Action) -> None:
    description = "Read image from file, find faces, and display in popup"
    parser: argparse.ArgumentParser = subparsers.add_parser(
        'faces', description=description, help=description)
    parser.add_argument('-i', '--input-file', required=True,
                        type=argparse.FileType(mode='rb', bufsize=4096))


def boxcss_to_rect(boxcss: tuple[int, int, int, int]) -> rectangle:
    """
    Convert a tuple in (top, right, bottom, left) order (= CSS order) to a dlib `rect` object

    :param boxcss:  plain tuple representation of the rect in (top, right, bottom, left) order
    :return: a dlib `rect` object
    """
    return rectangle(boxcss[3], boxcss[0], boxcss[1], boxcss[2])


def point_to_tuple(pt: point) -> tuple[int, int]:
    return (pt.x, pt.y)


def rgb_to_tuple(rgb: rgb_pixel) -> tuple[int, int, int]:
    return (rgb.red, rgb.green, rgb.blue)


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

    faces_boxes = fr.face_locations(img, number_of_times_to_upsample=FACES_DETECTION_UPSAMPLES,
                                    model=FACES_DETECTION_MODEL)

    faces_feat = fr.face_encodings(img, faces_boxes, FACES_ENCODINGS_JITTERS)
    assert len(faces_boxes)==len(faces_feat)
    faces_distances = [
        (
            fr.face_distance([faces_feat[box1_idx]], faces_feat[box2_idx]),
            box1_idx,
            box2_idx,
        )
        for box1_idx in range(len(faces_boxes)-1)
        for box2_idx in range(box1_idx+1, len(faces_boxes))
    ]
    faces_distances.sort(key=lambda _: _[0])

    faces_rect = [boxcss_to_rect(_) for _ in faces_boxes]
    for rect in faces_rect:
        _logger.debug("%r - %r", rect.bl_corner(), rect.tr_corner())
        cv.rectangle(img, point_to_tuple(rect.bl_corner()), point_to_tuple(rect.tr_corner()),
                     rgb_to_tuple(BOX_COLOR), BOX_THICKNESS)

    best_count = min(5, len(faces_distances))
    for best_idx in range(best_count):
        best_twin = faces_distances[best_idx]
        # twin_color: tuple[int, int, int] = tuple(int(_*(1-best_idx*.05)) for _ in rgb_to_tuple(BOX_COLOR_HIGHLIGHT))
        # twin_color: tuple[int, int, int] = rgb_to_tuple(BOX_COLOR_HIGHLIGHT)
        highlight_intensity = int(255*(1-best_idx*.10))
        _logger.debug("%r=", highlight_intensity)
        twin_color: tuple[int, int, int] = (0, 0, highlight_intensity)
        for rect in [faces_rect[best_twin[1]], faces_rect[best_twin[2]]]:
            bottom_left = point_to_tuple(rect.bl_corner())
            top_right = point_to_tuple(rect.tr_corner())
            cv.rectangle(img, bottom_left, top_right, twin_color, BOX_THICKNESS)
            text_x: int = top_right[0]+FONT_WIDTH*(best_idx % 2)
            best_rate: float = 1-best_idx/(best_count-1)
            text_y: int = int(bottom_left[1]*best_rate + top_right[1]*(1-best_rate) + FONT_HEIGHT/2)
            cv.putText(img, text=f"{best_idx}", org=(text_x, text_y),
                       fontFace=FONT_FACE, fontScale=FONT_SCALE,
                       color=(64, 64, 64), thickness=FONT_THICKNESS+3)
            cv.putText(img, text=f"{best_idx}", org=(text_x, text_y),
                       fontFace=FONT_FACE, fontScale=FONT_SCALE,
                       color=(255, 255, 255), thickness=FONT_THICKNESS)

    (height, width) = img.shape[:2]
    _logger.info("%rx%r", width, height)
    size_ratio: float = min(MAX_DISPLAY_WIDTH / width, MAX_DISPLAY_HEIGHT / height)
    display_img = cv.resize(src=img, dsize=None, fx=size_ratio, fy=size_ratio)

    _logger.debug("Displaying image")
    cv.imshow("Display window", display_img)
    _ = cv.waitKey(0)
