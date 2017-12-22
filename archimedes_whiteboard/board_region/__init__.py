"""
Tools for detecting, extracting, and normalizing the whiteboard region from
posted ArUco markers.
"""

from archimedes_whiteboard.board_region.internals import (get_all_markers)


def get_whiteboard_region_normal(whiteboard_image):
    """
    Get the region of the whiteboard marked by ArUco markers, crop to size,
    and get an approximated "head on" view by undoing the camera's
    perspective transform.
    """
    pass


__all__ = [
    'get_all_markers'
]
