"""
Test board region extraction functions.
"""

import cv2
from .. import board_region


img = cv2.imread('../../sample_images/1-angled.jpg')
markers = board_region.get_all_markers(img)
corners, ids, rejected = markers
img_with_markers = cv2.aruco.drawDetectedMarkers(img, corners, ids)
cv2.imshow("markers", img_with_markers)
