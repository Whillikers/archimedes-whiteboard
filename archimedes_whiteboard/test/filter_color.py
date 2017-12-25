"""
Test color filtering.

Useful for trying different threshold values for color filters to catch
different pen colors.
"""

import cv2
from archimedes_whiteboard.commands import region_extraction


img = cv2.imread('../sample_images/1-straight.jpg')

# Target blue, default tolerances
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
filtered = region_extraction.filter_to_color(hsv, 120)

resized = cv2.resize(filtered,
                     (1600, int(1600 * len(filtered) / len(filtered[0]))))

cv2.imshow('image', resized)
while True:
    if cv2.waitKey(1) == ord('q'):
        break
