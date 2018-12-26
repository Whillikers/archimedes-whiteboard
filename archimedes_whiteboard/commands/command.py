"""
Implements Command abstract base class.
"""

from archimedes_whiteboard.commands import region_extraction
from archimedes_whiteboard.commands.block_region import Block_Region


class Command():
    """
    Base class for commands that act on whiteboard regions.

    Not to be instantiated directly; use only as a base class for other
    commands. All commands cannot be instantiated directly; objects are
    created through YAML config.
    """

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
    blocked_regions = []    # Block_Regions that must be not colored to unblock
    cooldown_frames = 30    # Frames after a command before possibly unblocking
    block_clear_frames = 5  # Frames corners must be clear before unblocking
    block_clear_pixels = 3  # Pixels surrounding target corners to unblock

    yaml_tag = u'!Command'

    def __init__(self, target_hue, min_saturation=10, min_value=50,
                 max_dist_fraction=0.05, box_min_size=1000, blur_size=21,
                 dilate_size=5, cooldown_frames=30, block_reset_frames=5,
                 block_check_pixels=3):
        """
        Load the command's configuration.
        """
        self.target_hue = target_hue
        self.min_saturation = min_saturation
        self.min_value = min_value
        self.max_dist_fraction = max_dist_fraction
        self.box_min_size = box_min_size
        self.blur_size = blur_size
        self.dilate_size = dilate_size
        self.cooldown_frames = cooldown_frames
        self.block_reset_frames = block_reset_frames
        self.block_check_pixels = block_check_pixels
        self.blocked_regions = []

    def evaluate(self, command_region):
        """
        Implement this command's behavior when acting on a region.

        :param command_region: an image of the region to act on
        :type command_region: opencv bgr image
        """
        pass

    def get_image_blocked(self, image):
        """
        Given an image, update all Block_Regions and return the image with all
        blocked areas masked in white.
        """
        new_image = image
        for region in self.blocked_regions:
            region.update(image)
            new_image = region.mask_region(new_image)

        # Remove clear regions
        self.blocked_regions = list(filter(lambda x: not x.is_clear(),
                                           self.blocked_regions))
        return new_image

    def act_on_frame(self, image):
        """
        Given an image, find all regions that correspond to this command
        and act on them.

        Assumes that image is normalized.
        Uses, updates, and creates Block_Regions.

        :param image: the input image
        :type image: opencv bgr image
        """
        blocked = self.get_image_blocked(image)
        filtered = region_extraction.filter_to_color(blocked,
                                                     self.target_hue,
                                                     self.tol_hue,
                                                     self.min_saturation,
                                                     self.min_value)

        boxes = region_extraction.get_rectangular_boxes(filtered,
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
            block = Block_Region(
                [(xmin, ymin), (xmin, ymax), (xmax, ymin), (xmax, ymax)],
                self.target_hue,
                self.block_clear_frames, self.block_clear_pixels,
                self.cooldown_frames,
                self.tol_hue, self.min_saturation, self.min_value)
            self.blocked_regions.append(block)

        for region in regions:
            self.evaluate(region)
