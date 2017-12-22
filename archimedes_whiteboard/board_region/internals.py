"""
Backend for board region extraction.
"""

#  import cv2.aruco
import cv2


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
