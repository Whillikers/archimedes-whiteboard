#!/usr/bin/env python3
'''
    generate_marker.py

    Generates an ArUco marker image from the 6X6_250 OpenCV dictionary of a
    given id with 700 border pixels. See: www.philipzucker.com/aruco-in-opencv/
'''

import cv2

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
id = input('Enter ArUco id: ')
img = cv2.aruco.drawMarker(aruco_dict, id, 700)
cv2.imwrite('marker' + str(id) + '.jpg', img)
