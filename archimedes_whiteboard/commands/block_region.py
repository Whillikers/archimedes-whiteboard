"""
Implements Block_Region class.
"""

import numpy as np
import cv2
from archimedes_whiteboard.commands.region_extraction import filter_to_color


class Block_Region():
    """
    Region on an image that's blocked.
    Keeps track of frames remaining to unblock, corner properties, etc.
    """

    # Region location
    upper_left = (0, 0)
    lower_right = (0, 0)

    # Region-clearing properties
    clear_frames = 5  # Frames corners must be clear before unblocking
    clear_pixels = 10  # Pixels surrounding target corners to unblock

    # Color properties match command
    target_hue = None
    tol_hue = 35
    min_saturation = 10
    min_value = 50

    cooldown_frames_remaining = 30
    clear_frames_remaining = clear_frames  # Frames corners must be clear

    def __init__(self, corners, target_hue,
                 clear_frames=5, clear_pixels=10, cooldown_frames=30,
                 tol_hue=35, min_saturation=10, min_value=50):
        """
        Create a Block_Region.
        """

        self.corners = corners
        x_vals, y_vals = zip(*corners)
        self.x_min = min(x_vals)
        self.x_max = max(x_vals)
        self.y_min = min(y_vals)
        self.y_max = max(y_vals)

        self.clear_frames = clear_frames
        self.clear_pixels = clear_pixels
        self.cooldown_frames_remaining = cooldown_frames
        self.clear_frames_remaining = clear_frames
        self.target_hue = target_hue
        self.tol_hue = tol_hue
        self.min_saturation = min_saturation
        self.min_value = min_value

    def mask_region(self, image):
        """
        Given an image, return the image with the region blocked out in white.
        """
        c = self.clear_pixels
        new_image = image.copy()
        fill = cv2.rectangle(new_image,
                             (self.x_min - c, self.y_min - c),
                             (self.x_max + c, self.y_max + c),
                             (255, 255, 255), thickness=-1)
        return fill

    def are_corners_clear(self, image):
        """
        Check if all corners in this image are white.
        """
        filtered = filter_to_color(image, self.target_hue, self.tol_hue,
                                   self.min_saturation, self.min_value)

        for x, y in self.corners:
            if np.any(filtered[y - self.clear_pixels:y + self.clear_pixels,
                               x - self.clear_pixels:x + self.clear_pixels]):
                return False

        return True

    def update(self, image):
        """
        Updates frame counters, checking image to see if the corners are clear.

        :param image: an image to check the corners of
        :type image: opencv bgr image
        """
        if self.are_corners_clear(image):
            self.clear_frames_remaining -= 1
        else:
            self.clear_frames_remaining = self.clear_frames

        self.cooldown_frames_remaining -= 1

    def is_clear(self):
        """
        Returns true if the region has been clear for long enough to unblock.
        """
        return self.cooldown_frames_remaining <= 0 and \
            self.clear_frames_remaining <= 0
