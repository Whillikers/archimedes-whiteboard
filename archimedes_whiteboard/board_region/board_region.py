'''
Backend for board region extraction.
'''

import cv2
import numpy as np


# Initialize ArUco data
ARUCO_DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
ARUCO_PARAMETERS = cv2.aruco.DetectorParameters_create()


def get_all_markers(image):
    '''
    Get all ArUco markers in an image in the format (corners, ids, rejected).

    Parameters
    ----------
    image : opencv bgr image
        The image.

    Returns
    -------
    3-tuple in the format (corners, ids, rejected) returned by detectMarkers
        All ArUco markers visible in the image.
    '''
    return cv2.aruco.detectMarkers(image, ARUCO_DICTIONARY,
                                   parameters=ARUCO_PARAMETERS)


def get_marker_inverse_transform(corners):
    '''
    Get the transformation that maps a marker to a square of the same width.

    This is an approximate inverse perspective transform from the camera's
    pose to get a "head-on" view of the board given ArUco markers.

    Parameters
    ----------
    corners : 4-tuple of 2-tuples
        The corners of an ArUco marker.

    Returns
    -------
    numpy array
        A perspective transform from the skewed marker to a square.
    '''
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
    '''
    Get a "head-on" view of an image with multiple visible markers.

    Approximately inverts the camera's perspective to the whiteboard using
    the average inverse transforms of at least two visible markers.

    Parameters
    ----------
    image : opencv bgr image
        The image.

    Returns
    -------
    opencv bgr image
        A head-on view of the image.
    '''
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

    return cv2.warpPerspective(image, avg_transform, (width * 2, height * 2))


def crop_image_to_markers(image):
    '''
    Crop an image with multiple ArUco markers to the outer rectangular region
    of those markers and white out the markers.

    Assumes only one marked region is present in the image, the region is
    roughly rectangular, and the region is not rotated much (i.e. it is
    normalized).

    Parameters
    ----------
    image : opencv bgr image
        An image with multiple aruco markers in a rectangular region.

    Returns
    -------
    opencv bgr image
        The image cropped to the rectangular region outside the markers.
    '''
    markers = get_all_markers(image)
    markers_corners = markers[0]

    corners_x, corners_y = [], []
    for corners in markers_corners:
        for corner in corners[0]:
            corners_x.append(corner[0])
            corners_y.append(corner[1])

        # White out marker
        image = cv2.rectangle(image,
                              (corners[0][0][0], corners[0][0][1]),
                              (corners[0][2][0], corners[0][2][1]),
                              (255, 255, 255),
                              thickness=-1)  # Indicates fill

    left_edge = int(min(corners_x))
    right_edge = int(max(corners_x))
    top_edge = int(min(corners_y))
    bottom_edge = int(max(corners_y))

    return image[top_edge:bottom_edge, left_edge:right_edge]
