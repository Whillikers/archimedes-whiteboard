'''
Implements Command abstract base class.
'''

from archimedes_whiteboard.commands.region_extraction import \
    (filter_to_color, get_rectangular_boxes)
from archimedes_whiteboard.commands.block_region import Block_Region


class Command():
    '''
    Base class for commands that act on whiteboard regions.

    Not to be instantiated directly; use only as a base class for other
    commands. All commands cannot be instantiated directly; objects are
    created through YAML config.

    Attributes
    ----------
    yaml_tag : unicode string
        YAML tag of this command. Used internally to map from YAML sections
        to classes and should be distinct for each different type of command.

    Parameters
    ----------
    target_hue : number
        The hue to be detected.
    tol_hue (optional) : number
        Range of acceptable hues around the target color.
    min_saturation (optional) : number
        Minimum saturation to detect the color.
    min_value (optional) : number
        Minimum value to detect the color.
    max_dist_fraction (optional) : number in [0, 1]
        Maximum distance the detected rectangle can be from the original
        contour as a fraction of contour perimeter.
    box_min_size (optional) : int
        Minimum area of a box to be detected (pixels).
    blur_size (optional) : odd int
        Size of gaussian blur to apply; used for denoising.
    dilate_size (optional) : int
        Size of dilation to apply; used for closing holes.
    cooldown_frames (optional) : positive int
        Absolute minimum number of frames before unblocking this region.
    block_clear_frames (optional) : positive int
        Number of frames for which corners must be clear before unblocking.
    block_clear_pixels (optional) : positive int
        Number of pixels surrounding target corners in each direction that
        must all be clear to unblock.
    '''

    yaml_tag = u'!Command'

    # Color parameters
    target_hue = None  # Mandatory
    tol_hue = 35
    min_saturation = 10
    min_value = 50

    # Box detection parameters
    max_dist_fraction = 0.05
    box_min_size = 1000
    blur_size = 21
    dilate_size = 5

    # Blocking parameters
    blocked_regions = []
    cooldown_frames = 30
    block_clear_frames = 5
    block_clear_pixels = 10

    def _evaluate(self, command_region):
        '''
        Implement this command's behavior when acting on a region.

        Parameters
        ----------
        command_region : opencv bgr image
            An image of the region to act on.
        '''
        pass

    def _get_image_blocked(self, image):
        '''
        Given an image, update all Block_Regions and return the image with all
        blocked areas masked in white.

        Parameters
        ----------
        image : opencv bgr image
            A normalized image of the full whiteboard.

        Returns
        -------
        opencv bgr image
            The input image, with all Block_Regions masked in white.
        '''
        new_image = image.copy()

        for region in self.blocked_regions:
            region.update(image)
            new_image = region.mask_region(new_image)

        # Remove clear regions
        self.blocked_regions = list(filter(lambda x: not x.is_clear(),
                                           self.blocked_regions))
        return new_image

    def act_on_frame(self, image):
        '''
        Given an image, find all regions that correspond to this command
        and act on them.

        Assumes that image is normalized.
        Uses, updates, and creates Block_Regions.

        Parameters
        ----------
        image : opencv bgr image
            The input image.
        '''
        blocked = self._get_image_blocked(image)
        filtered = filter_to_color(blocked,
                                   self.target_hue,
                                   self.tol_hue,
                                   self.min_saturation,
                                   self.min_value)

        boxes = get_rectangular_boxes(filtered,
                                      self.max_dist_fraction,
                                      self.box_min_size,
                                      self.blur_size,
                                      self.dilate_size)

        regions = []
        for box in boxes:
            xmin = min(box, key=lambda x: x[0][0])[0][0]
            xmax = max(box, key=lambda x: x[0][0])[0][0]
            ymin = min(box, key=lambda x: x[0][1])[0][1]
            ymax = max(box, key=lambda x: x[0][1])[0][1]
            regions.append(image[ymin:ymax, xmin:xmax])
            corners = [tuple(corner[0]) for corner in box]
            block = Block_Region(corners,
                                 self.target_hue,
                                 self.block_clear_frames,
                                 self.block_clear_pixels,
                                 self.cooldown_frames,
                                 self.tol_hue,
                                 self.min_saturation,
                                 self.min_value)
            self.blocked_regions.append(block)

        for region in regions:
            self._evaluate(region)
