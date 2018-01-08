"""
Implements a command that saves an image locally.
"""

import time
import yaml
import cv2
from archimedes_whiteboard.commands import command


class SavePicture(command.Command, yaml.YAMLObject):
    """
    Command that saves identified regions as images locally.
    """

    yaml_tag = u'!SavePicture'
    img_id = 0  # Prevent same-time name collision

    def __init__(self, directory):
        command.Command.__init__()
        self.directory = directory

    def evaluate(self, command_region):
        """
        Save the command region in the specified directory.

        :param command_region: an image of the region to act on
        :type command_region: opencv bgr image
        """
        name = time.strftime('%Y-%m-%d,%H:%M:%S', time.gmtime())
        path = self.directory + '/' + name + ',' + str(self.img_id) + '.png'
        self.img_id += 1
        cv2.imwrite(path, command_region)
