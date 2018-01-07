"""
Test rectangle detection.

Useful for tuning command region detection for your setup.
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from archimedes_whiteboard.commands import region_extraction
from archimedes_whiteboard.board_region import get_whiteboard_region_normal

img = cv2.imread('../sample_images/2-thicklines-angled.jpg')
normalized = get_whiteboard_region_normal(img)

filtered = region_extraction.filter_to_color(normalized, 180,
                                             tol_hue=20,
                                             min_saturation=30,
                                             min_value=150)

rectangles = region_extraction.get_rectangular_boxes(filtered,
                                                     blur_size=21,
                                                     dilate_size=5)

blank = np.zeros((len(filtered), len(filtered[0])), np.uint8)

plt.figure(1)
plt.tight_layout()
plt.subplot(221)
plt.imshow(img, cmap = 'gray', interpolation = 'none')
plt.subplot(222)
plt.imshow(normalized, cmap = 'gray', interpolation = 'none')
plt.subplot(223)
plt.imshow(filtered, cmap = 'gray', interpolation = 'none')
plt.subplot(224)
for rect in rectangles:
    cv2.polylines(blank, rect, True, (255, 255, 255), 10)
plt.imshow(blank, cmap = 'gray', interpolation = 'none')
plt.show()
