'''
Implements Block_Region class.
'''

import numpy as np
import cv2
from archimedes_whiteboard.commands.region_extraction import filter_to_color


class Block_Region():
    '''
    Region on an image that's blocked.

    Keeps track of frames remaining to unblock, corner properties, etc.

    Parameters
    ----------
    corners : 4-tuple of (x, y) 2-tuples
        Corners of the region. Not necessarily axis-aligned rectangular.
    target_hue : number
        The hue to be detected.
    clear_frames (optional) : positive int
        Number of frames for which corners must be clear before unblocking.
    clear_pixels (optional) : positive int
        Number of pixels surrounding target corners in each direction that
        must all be clear to unblock.
    cooldown_frames (optional) : positive int
        Absolute minimum number of frames before unblocking this region.
    tol_hue (optional) : number
        Range of acceptable hues around the target color.
    min_saturation (optional) : number
        Minimum saturation to detect the color.
    min_value (optional) : number
        Minimum value to detect the color.
    '''

    def __init__(self, corners, target_hue,
                 clear_frames=5, clear_pixels=10, cooldown_frames=30,
                 tol_hue=35, min_saturation=10, min_value=50):
        self._corners = corners
        x_vals, y_vals = zip(*corners)
        self._x_min = min(x_vals)
        self._x_max = max(x_vals)
        self._y_min = min(y_vals)
        self._y_max = max(y_vals)

        self._clear_frames = clear_frames
        self._clear_pixels = clear_pixels
        self._cooldown_frames_remaining = cooldown_frames
        self._clear_frames_remaining = clear_frames

        # Color properties match command
        self._target_hue = target_hue
        self._tol_hue = tol_hue
        self._min_saturation = min_saturation
        self._min_value = min_value

    def _are_corners_clear(self, image):
        '''
        Check if all corners in this image are clear.

        Parameters
        ----------
        image : opencv bgr image
            The input image.

        Returns
        -------
        bool
            True if all the corners in the image are white, False otherwise.
        '''
        filtered = filter_to_color(image, self._target_hue, self._tol_hue,
                                   self._min_saturation, self._min_value)

        for x, y in self._corners:
            if np.any(filtered[y - self._clear_pixels:y + self._clear_pixels,
                               x - self._clear_pixels:x + self._clear_pixels]):
                return False

        return True

    def mask_region(self, image):
        '''
        Given an image, return the image with the region blocked out in white.

        Parameters
        ----------
        image : opencv bgr image
            The input image.

        Returns
        -------
        opencv bgr image
            A copy of the input image, with this region blocked out in white.
        '''
        c = self._clear_pixels
        fill = cv2.rectangle(image.copy(),
                             (self._x_min - c, self._y_min - c),
                             (self._x_max + c, self._y_max + c),
                             (255, 255, 255), thickness=-1)
        return fill

    def update(self, image):
        '''
        Updates frame counters, checking image to see if the corners are clear.

        Parameters
        ----------
        image : opencv bgr image
            An image to check the corners of.
        '''
        if self._are_corners_clear(image):
            self._clear_frames_remaining -= 1
        else:
            self._clear_frames_remaining = self._clear_frames

        self._cooldown_frames_remaining -= 1

    def is_clear(self):
        '''
        Returns whether the region has been clear for long enough to unblock.

        Returns
        -------
        bool
            True if the region is unblocked, False otherwise.
        '''
        return self._cooldown_frames_remaining <= 0 and \
            self._clear_frames_remaining <= 0
