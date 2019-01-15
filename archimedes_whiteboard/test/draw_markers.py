'''
Test board region extraction functions.
'''

import cv2
from archimedes_whiteboard import board_region


img = cv2.imread('../sample_images/sideangle_highres.jpg')

markers = board_region.get_all_markers(img)
corners, ids, rejected = markers
img_with_markers = cv2.aruco.drawDetectedMarkers(img, corners, ids)

resized = cv2.resize(img_with_markers, (1600, 1600))
cv2.imshow("markers", resized)
cv2.waitKey(0)  # Window closes on key press
