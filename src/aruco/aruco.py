"""ArUco module for ArUcoNavSystem

This module is needed to detect, get position and data from the ArUco marker.

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import cv2
import math
from utils.utils import draw_bounding_box, draw_marker_data
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

def estimatePose(corners, marker_size, mtx, distortion):
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    
    trash = []
    rvecs = []
    tvecs = []
    i = 0
    for c in corners:
        nada, R, t = cv2.solvePnP(marker_points, corners[i], mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6
 
# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :
 
    assert(isRotationMatrix(R))
 
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
 
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return np.array([x, y, z])

def detect_marker(img, w, mtx, dist, aruco_dict = cv2.aruco.DICT_7X7_1000):
    marker_list = []
    corners, ids, _ = cv2.aruco.detectMarkers(img, cv2.aruco.Dictionary_get(aruco_dict))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if len(corners) > 0:
        for mcorner, mid in zip(corners, ids):
            # marker corner extraction and to x,y coordinates conversion
            cv2.cornerSubPix(gray, mcorner, winSize = (3,3), zeroZone = (-1,-1), criteria = criteria)
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
            marker_size = 0.035
            measured_distance = 0.3
            conversion_factor = measured_distance / marker_size
            
            #rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(mcorner, 0.035, mtx, dist)
            
            rvecs, tvecs, _ = estimatePose(mcorner, 0.035, mtx, dist)
            
            #distance = np.linalg.norm(tvecs[0][0][2])
            rmat, _ = cv2.Rodrigues(rvecs[0])
            
            xyz = rotationMatrixToEulerAngles(rmat)

            marker_data = {'id': mid[0], 'yaw': round(0)}
            marker_list.append(marker_data)
            
            distancestr = f"Distance: {str(round(tvecs[0][2][0]*70))} cm"
            yawstr = f"Yaw Degrees: {round(math.degrees(xyz[1]))}"
            rollstr = f"Roll Degrees: {round(math.degrees(xyz[2]))}"
            cv2.putText(img, distancestr, (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(img, yawstr, (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(img, rollstr, (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            img = draw_bounding_box(img, top_left, top_right, bottom_left, bottom_right)
            img = draw_marker_data(img, top_left, f'Roll: {rotation_angle}, Yaw: {0}, Side: {side}, Distance: {0}')
    return img, marker_list
            