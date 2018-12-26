"""
Test the commands backend and region blocking.
"""

import yaml
import cv2
from archimedes_whiteboard.commands.tasks import save_picture
from archimedes_whiteboard.board_region import get_whiteboard_region_normal

img = cv2.imread('../sample_images/2-thicklines-angled.jpg')
normalized = get_whiteboard_region_normal(img)

with open('../tasks.yml') as config:
    commands = list(yaml.load_all(config))
    command = commands[0]

command.cooldown_frames = 3
command.block_clear_frames = 3

command.act_on_frame(normalized)  # Should act on all boxes
for _ in range(3):
    command.act_on_frame(normalized)  # Should do nothing
command.act_on_frame(normalized)  # Should act on all boxes
