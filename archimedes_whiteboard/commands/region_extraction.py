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
    :type image: opencv bgr image
    :param target_hue: the hue to be detected
    :type target_hue: number
    :param tol_hue: range of acceptable hues around the target color
    :type tol_hue: number
    :param min_saturation: minimum saturation to detect the color
    :type min_saturation: number
    :param min_value: minimum value to detect the color
    :type min_value: number
    :returns: an image only containing pixels that are the specified color
    :rtype: opencv grayscale image
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_color = np.array([target_hue - tol_hue, min_saturation, min_value])
    high_color = np.array([target_hue + tol_hue, 255, 255])
    return cv2.inRange(image, low_color, high_color)


def get_rectangular_boxes(image,
                          max_dist_fraction=0.05,
                          min_size=1000,
                          blur_size=0,
                          dilate_size=0):
    """
    Find all rectangular boxes in an image.

    To be used after filtering to a color to get all command regions of a
    specific color. Returns a list of rectangles, each as a four-tuple of its
    corner coordinates.

    :param image: the image
    :type image: opencv grayscale image
    :param max_dist_fraction: maximum distance the detected rectangle can be
    from the original contour as a fraction of contour perimeter
    :type max_dist_fraction: number in [0, 1]
    :param min_size: minimum area of a rectangle to be detected (pixels)
    :type min_size: int
    :param blur_size: size of gaussian blur to apply; used for denoising
    :type blur_size: odd int
    :param dilate_size: size of dilation to apply; used for closing holes
    :type dilate_size: int
    :returns: a list of detected rectangles as their corners
    :rtype: array
    """
    # For technique, see:
    # https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/ and
    # https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
    if blur_size > 0:
        image = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
    image = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)[1]
    if dilate_size > 0:
        kernel = np.ones((dilate_size, dilate_size))

        # Open to remove noise, then dilate to connect box components
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        image = cv2.dilate(image, kernel, iterations=1)

    contours = cv2.findContours(image.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[1]

    rectangles = []
    for contour in contours:
        # Filter by area
        if cv2.contourArea(contour) < min_size:
            continue

        epsilon = max_dist_fraction * cv2.arcLength(contour, closed=True)
        polygon_approx = cv2.approxPolyDP(contour, epsilon, closed=True)

        if len(polygon_approx) == 4:  # Count corners
            rectangles.append(polygon_approx)

    return rectangles
