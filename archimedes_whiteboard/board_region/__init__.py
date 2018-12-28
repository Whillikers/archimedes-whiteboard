'''
Tools for detecting, extracting, and normalizing the whiteboard region from
posted ArUco markers.
'''

from archimedes_whiteboard.board_region.board_region import (
    crop_image_to_markers,
    get_all_markers,
    normalize_image
)


def get_whiteboard_region_normal(whiteboard_image):
    '''
    Get a cropped and normalized view of the designated smart region.

    Assumes the region is marked off by four ArUco markers.
    Results in an approximated "head-on" view cropped to the outer boundary
    of the marked-off region.

    Parameters
    ----------
    whiteboard_image : opencv bgr image
        A whiteboard image with four ArUco markers.

    Returns
    -------
    opencv bgr image
        The image normalized and cropped to the designated region.
    '''
    normal = normalize_image(whiteboard_image)
    cropped = crop_image_to_markers(normal)
    return cropped


__all__ = [
    'get_whiteboard_region_normal',
    'get_all_markers',
    'normalize_image',
    'crop_image_to_markers'
]
