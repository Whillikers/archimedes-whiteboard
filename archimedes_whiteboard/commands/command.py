"""
Implements Command abstract base class.
"""

from archimedes_whiteboard.commands import region_extraction


class Command():
    """
    Base class for commands that act on whiteboard regions.

    Not to be instantiated directly; use only as a base class for other
    commands.
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

    yaml_tag = u'!Command'

    def __init__(self, target_hue, min_saturation=10, min_value=50,
                 max_dist_fraction=0.05, box_min_size=1000, blur_size=21,
                 dilate_size=5):
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

    def evaluate(self, command_region):
        """
        Implement this command's behavior when acting on a region.

        :param command_region: an image of the region to act on
        :type command_region: opencv bgr image
        """
        pass

    def act_on_frame(self, image):
        """
        Given an image, find all regions that correspond to this command
        and act on them.

        Assumes that image is normalized.

        :param image: the input image
        :type image: opencv bgr image
        """
        filtered = region_extraction.filter_to_color(image,
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

        for region in regions:
            self.evaluate(region)
