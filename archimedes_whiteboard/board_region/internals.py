"""
Backend for board region extraction.
"""

import cv2
import numpy as np


# Initialize ArUco data
ARUCO_DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
ARUCO_PARAMETERS = cv2.aruco.DetectorParameters_create()


def get_all_markers(image):
    """
    Get all ArUco markers in an image in the format (corners, ids, rejected).


    corners is an array of 4-tuples of points where each point is a corner of a
    marker.

    rejected is an array of contours rejected as marker candidates
    """
    return cv2.aruco.detectMarkers(image,
                                   ARUCO_DICTIONARY,
                                   parameters=ARUCO_PARAMETERS)


def get_marker_inverse_transform(corners):
    """
    Gets the transformation that maps a marker to a square of the same width.
    """
    top_left, top_right = corners[0], corners[1]
    side_length = top_right[0] - top_left[0]
    new_corners = np.array([
        top_left,
        (top_left[0] + side_length, top_left[1]),
        (top_left[0] + side_length, top_left[1] + side_length),
        (top_left[0], top_left[1] + side_length),
    ])
    return cv2.getPerspectiveTransform(corners, new_corners)


def normalize_image(image):
    """
    Approximately invert the effect of camera perspective to give a "head-on"
    view of the board given an image with multiple visible markers.
    """
    markers = get_all_markers(image)
    corners = markers[0]
    width = len(image[0])
    height = len(image)

    # Average the perspective inverse transforms for all four corner markers
    transforms = [get_marker_inverse_transform(corner[0])
                  for corner in corners]

    avg_transform = transforms[0]
    for transform in transforms[1:]:
        avg_transform += transform
    avg_transform /= len(transforms)

    return cv2.warpPerspective(image, avg_transform, (width, height))


def crop_image_to_markers(image):
    """
    Crop an image with four visible markers to the outer boundary of the
    rectangle defined by those markers.

    Assumes that the image lacks significant rotation (i.e. it is normalized).
    """
    markers = get_all_markers(image)
    markers_corners = markers[0]

    corners_x, corners_y = [], []
    for corners in markers_corners:
        for corner in corners[0]:
            corners_x.append(corner[0])
            corners_y.append(corner[1])
    left_edge = int(min(corners_x))
    right_edge = int(max(corners_x))
    top_edge = int(min(corners_y))
    bottom_edge = int(max(corners_y))

    return image[top_edge:bottom_edge, left_edge:right_edge]
