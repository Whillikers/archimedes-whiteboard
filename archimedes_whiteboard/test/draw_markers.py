"""
Test board marker detection.
"""

import cv2
from archimedes_whiteboard import board_region


img = cv2.imread('../sample_images/1-angled.jpg')

markers = board_region.get_all_markers(img)
corners, ids, rejected = markers
img_with_markers = cv2.aruco.drawDetectedMarkers(img, corners, ids)

resized = cv2.resize(img_with_markers, (1600, 1600))
cv2.imshow("markers", resized)
while True:
    if cv2.waitKey(1) == ord('q'):
        break
