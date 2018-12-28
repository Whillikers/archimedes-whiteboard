'''
Utilities for detecting and extracting command regions of different colors.
'''


import cv2
import numpy as np


def filter_to_color(image, target_hue, tol_hue=35, min_saturation=10,
                    min_value=50):
    '''
    Filter an image to get only a specific color.

    Returns an image with only pixels with hue within tol_hue of target_hue,
    of saturation at least min_saturation, and of value at least min_value.

    Parameters
    ----------
    image : opencv bgr image
        The input image.
    target_hue : number
        The hue to be detected.
    tol_hue (optional) : number
        Range of acceptable hues around the target color.
    min_saturation (optional) : number
        Minimum saturation to detect the color.
    min_value (optional) : number
        Minimum value to detect the color.

    Returns
    -------
    opencv grayscale image
        An image only containing pixels that are the specified color.
    '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_color = np.array([target_hue - tol_hue, min_saturation, min_value])
    high_color = np.array([target_hue + tol_hue, 255, 255])
    return cv2.inRange(image, low_color, high_color)


def get_rectangular_boxes(image,
                          max_dist_fraction=0.05,
                          min_size=1000,
                          blur_size=21,
                          dilate_size=5):
    '''
    Find all rectangular boxes in an image.

    To be used after filtering to a color to get all command regions of a
    specific color. Returns a list of rectangles, each as a four-tuple of its
    corner coordinates.

    Parameters
    ----------
    image : opencv grayscale image
        The image.
    max_dist_fraction (optional) : number in [0, 1]
        Maximum distance the detected rectangle can be from the original
        contour as a fraction of contour perimeter.
    min_size (optional) : int
        Minimum area of a rectangle to be detected (pixels).
    blur_size (optional) : odd int
        Size of gaussian blur to apply; used for denoising.
    dilate_size (optional) : int
        Size of dilation to apply; used for closing holes.

    Returns
    -------
    list
        A list of detected rectangles as their corners.
    '''
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
