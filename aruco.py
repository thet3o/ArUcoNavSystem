"""ArUco module for ArUcoNavSystem

This module is needed to detect, get position and data from the ArUco marker.

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import cv2
import utils


def get_marker_orientation(top_left, top_right, bottom_left, bottom_right):
    if top_left[1] > top_right[1]: 
        print('left') 
        return 'left'
    elif top_left[1] < top_right[1]: 
        print('right')
        return 'right'

def detect_marker(img, mtx, dist, aruco_dict = cv2.aruco.DICT_7X7_1000):
    corners, ids, _ = cv2.aruco.detectMarkers(img, cv2.aruco.Dictionary_get(aruco_dict), cameraMatrix=mtx, distCoeff=dist)
    
    if len(corners) > 0:
        for mcorner, mid in zip(corners, ids):
            # marker corner extraction and to x,y coordinates conversion
            mcorners = mcorner.reshape((4,2))
            top_left, top_right, bottom_right, bottom_left = mcorners
            
            top_left = (int(top_left[0]), int(top_left[1]))
            top_right = (int(top_right[0]), int(top_right[1]))
            bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            
            img = utils.draw_bounding_box(img, top_left, top_right, bottom_left, bottom_right)
            img = utils.draw_center(img, top_left, bottom_right)
            img = utils.draw_marker_data(img, top_left, (top_left, top_right, bottom_left, bottom_right))
            
    return img
            
            


if __name__ == '__main__':
    
    fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_READ)
    mtx = fs.getNode('camera_matrix').mat()
    dist = fs.getNode('dist_coeffs').mat()
    fs.release()
    
    cap = cv2.VideoCapture(1)
    
    while True:
        ret, img = cap.read()
        
        img = detect_marker(img, mtx, dist)
        cv2.imshow('debug', img)

            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()