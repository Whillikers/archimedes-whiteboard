'''
Test the commands backend and config loading.
'''

import yaml
import cv2
from archimedes_whiteboard.commands.tasks import save_picture  # NOQA
from archimedes_whiteboard.board_region import get_whiteboard_region_normal

img = cv2.imread('../sample_images/2-thicklines-angled.jpg')
normalized = get_whiteboard_region_normal(img)

with open('../tasks.yml') as config:
    commands = list(yaml.load_all(config))
    for task in commands:
        task.act_on_frame(normalized)
