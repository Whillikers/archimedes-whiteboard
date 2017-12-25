"""
Detecting and extracting command regions of different colors.
"""


import cv2
import numpy as np


def filter_to_color(image, target_hue, tol_hue=35, min_saturation=10,
                    min_value=50):
    """
    Filter an image to get only a specific color.

    Returns an image with only pixels with hue within tol_hue of target_hue,
    of saturation at least min_saturation, and of value at least min_value.

    :param image: the input image
    :type image: opencv hsv image
    :param target_hue: the hue to be detected
    :type target_hue: number
    :param tol_hue: range of acceptable hues around the target color
    :type tol_hue: number
    :param min_saturation: minimum saturation to detect the color
    :type min_saturation: number
    :param min_value: minimum value to detect the color
    :type min_value: number
    :returns: an image only containing pixels that are the specified color
    :rtype: opencv hsv image
    """
    low_color = np.array([target_hue - tol_hue, min_saturation, min_value])
    high_color = np.array([target_hue + tol_hue, 255, 255])
    return cv2.inRange(image, low_color, high_color)
