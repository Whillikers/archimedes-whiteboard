"""
Test board region normalization.
"""

import cv2
from archimedes_whiteboard import board_region


img = cv2.imread('../sample_images/1-angled.jpg')
normalized = board_region.get_whiteboard_region_normal(img)
resized = cv2.resize(normalized,
                     (1600, int(1600 * len(normalized) / len(normalized[0]))))

cv2.imshow('image', resized)
while True:
    if cv2.waitKey(1) == ord('q'):
        break
