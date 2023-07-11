"""ArUco module for ArUcoNavSystem

This module is needed to detect, get position and data from the ArUco marker.

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import cv2
import math
import utils
import numpy as np

# https://github.com/fayyazpocker/ArUco-marker-detection/blob/master/aruco_lib.py
def angle_calculate(pt1,pt2, trigger = 0):  # function which returns angle between two points in the range of 0-359
    angle_list_1 = list(range(359,0,-1))
    #angle_list_1 = angle_list_1[90:] + angle_list_1[:90]
    angle_list_2 = list(range(359,0,-1))
    angle_list_2 = angle_list_2[-90:] + angle_list_2[:-90]
    x=pt2[0]-pt1[0] # unpacking tuple
    y=pt2[1]-pt1[1]
    angle=int(math.degrees(math.atan2(y,x))) #takes 2 points nad give angle with respect to horizontal axis in range(-180,180)
    if trigger == 0:
        angle = angle_list_2[angle]
    else:
        angle = angle_list_1[angle]
    return int(angle)


def side_position(x, w):
    return 'left' if x < w/2 else 'right'
        

def detect_marker(img, w, mtx, dist, aruco_dict = cv2.aruco.DICT_7X7_1000):
    corners, ids, _ = cv2.aruco.detectMarkers(img, cv2.aruco.Dictionary_get(aruco_dict))
    
    if len(corners) > 0:
        for mcorner, mid in zip(corners, ids):
            # marker corner extraction and to x,y coordinates conversion
            mcorners = mcorner.reshape((4,2))
            top_left, top_right, bottom_right, bottom_left = mcorners
            
            x = (top_left[0] + top_right[0] + bottom_right[0] + bottom_left[0]) / 4
            y = (top_left[1] + top_right[1] + bottom_right[1] + bottom_left[1]) / 4
            
            side = side_position(x, w)
            
            top_left = (int(top_left[0]), int(top_left[1]))
            top_right = (int(top_right[0]), int(top_right[1]))
            bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            rotation_angle = angle_calculate(top_left, bottom_left)
            
            ### Distance data
            marker_size = 0.04
            measured_distance = 0.3
            conversion_factor = measured_distance / marker_size
            #(tvec[0][0][2])
            
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(mcorner, 0.04, mtx, dist)
            distance = np.linalg.norm(tvec[0][0][2]) 
            img = utils.draw_bounding_box(img, top_left, top_right, bottom_left, bottom_right)
            img = utils.draw_marker_data(img, top_left, f'Rotation angle: {rotation_angle}, Side: {side}, Distance: {(distance*conversion_factor)}')
    return img
            

if __name__ == '__main__':
    
    fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_READ)
    mtx = fs.getNode('camera_matrix').mat()
    dist = fs.getNode('dist_coeffs').mat()
    fs.release()
    
    cap = cv2.VideoCapture(1)
    
    while True:
        ret, img = cap.read()
        h, w, _ = img.shape
        
        img = detect_marker(img, w, mtx, dist)
            
        cv2.imshow('debug', img)

            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()