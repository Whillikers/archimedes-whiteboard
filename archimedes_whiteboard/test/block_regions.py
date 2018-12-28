'''
Test the Block_Region class.
'''

import cv2
from archimedes_whiteboard.commands import region_extraction
from archimedes_whiteboard.commands.block_region import Block_Region

img = cv2.imread('../sample_images/1-straight.jpg')

# Target blue, default tolerances
filtered = region_extraction.filter_to_color(img, 120)
resized = cv2.resize(img, (1600, int(1600 * len(img) / len(img[0]))))

region = Block_Region([(320, 348), (473, 332), (330, 400), (482, 394)], 120)
blocked = region.mask_region(resized)

cv2.imshow('blocked', blocked)

print('Base image clear?', region._are_corners_clear(resized))
print('Masked image clear?', region._are_corners_clear(blocked))

while True:
    if cv2.waitKey(1) == ord('q'):
        break
