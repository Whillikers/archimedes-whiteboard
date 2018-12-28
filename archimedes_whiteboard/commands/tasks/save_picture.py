'''
Implements a command that saves an image locally.
'''

import time
import yaml
import cv2
from archimedes_whiteboard.commands import command


class SavePicture(command.Command, yaml.YAMLObject):
    '''
    Command that saves identified regions as images locally.

    Cannot be instantiated directly; objects are created through YAML config.

    Parameters
    ----------
    directory : str path to a directory
        Directory to save images in.
    '''

    yaml_tag = u'!SavePicture'
    _img_id = 0  # Prevent same-time name collision

    def _evaluate(self, command_region):
        '''
        Save the command region in the specified directory.

        Parameters
        ----------
        command_region : opencv bgr image
            An image of the region to act on.
        '''
        name = time.strftime('%Y-%m-%d,%H:%M:%S', time.gmtime())
        path = self.directory + '/' + name + '_' + str(self._img_id) + '.png'
        self._img_id += 1
        cv2.imwrite(path, command_region)
