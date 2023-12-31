"""ArUco module for ArUcoNavSystem

This module is needed to detect, get position and data from the ArUco marker.
The calibration is needed to permit a correct estimation of rotation and transformation vectors.

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import cv2
import math
from utils.utils import draw_bounding_box, draw_marker_data
import numpy as np


def estimate_pose(corners, marker_size, mtx, distortion):
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
def is_rotation_matrix(R) :
    Rt = np.transpose(R)
    should_be_identity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - should_be_identity)
    return n < 1e-6
 
def rotmat_to_euler(R) :
 
    assert(is_rotation_matrix(R))
 
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


def calculate_rotation(yaw, tvecs, final):
    correction_angle = final
    correction_angle -= round(yaw)
    side = ''
    if tvecs[0][0] < 0.08:
        #print(f'Rotate right {correction_angle} degrees')
        side = 'left'
        rotation_direction = 'right'
    else:
        #print(f'Rotate left {correction_angle} degrees')
        side = 'right'
        rotation_direction = 'left'
    
    return correction_angle, side, rotation_direction

def yawpitchrolldecomposition(R):
    sin_x    = math.sqrt(R[2,0] * R[2,0] +  R[2,1] * R[2,1])    
    validity  = sin_x < 1e-6
    if not validity:
        z1    = math.atan2(R[2,0], R[2,1])     # around z1-axis
        x      = math.atan2(sin_x,  R[2,2])     # around x-axis
        z2    = math.atan2(R[0,2], -R[1,2])    # around z2-axis
    else: # gimbal lock
        z1    = 0                                         # around z1-axis
        x      = math.atan2(sin_x,  R[2,2])     # around x-axis
        z2    = 0                                         # around z2-axis

    return np.array([[z1], [x], [z2]])

def detect_marker(img, mtx, dist, aruco_dict = cv2.aruco.DICT_7X7_1000):
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
            
            
            top_left = (int(top_left[0]), int(top_left[1]))
            top_right = (int(top_right[0]), int(top_right[1]))
            bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            #sea 0.035
            rvecs, tvecs, _ = estimate_pose(mcorner, 0.140, mtx, dist)
            
            rmat, _ = cv2.Rodrigues(rvecs[0])
            
            xyz = rotmat_to_euler(rmat)
            #heading_correction, side, rotation_direction = calculate_rotation(abs(math.degrees(xyz[1])), tvecs,90)
            
            
            yawpitchroll_angles = -180*yawpitchrolldecomposition(rmat)/math.pi
            #yawpitchroll_angles[0,0] = (360-yawpitchroll_angles[0,0])%360 # change rotation sense if needed, comment this line otherwise
            yawpitchroll_angles[1,0] = yawpitchroll_angles[1,0]+90
            heading_correction, side, rotation_direction = calculate_rotation(abs(yawpitchroll_angles[0][0]), tvecs,90)
            # Data
            distance = round(tvecs[0][2][0]*70) # unit is cm
            yaw = round(math.degrees(xyz[1]))
            roll = round(math.degrees(xyz[0]))
            
            cv2.drawFrameAxes(img, mtx, dist, rvecs[0], tvecs[0], 0.1, 2)
            
            # Data visualization
            distancestr = f"Distance: {distance} cm"
            yawstr = f"Yaw Degrees: {round(yawpitchroll_angles[0][0])}"
            rollstr = f"Roll Degrees: {roll}"
            
            marker_data = {'id': mid[0], 'distance': distance, 'yaw': round(yawpitchroll_angles[0][0]), 'roll': roll}
            marker_list.append(marker_data)
            
            cv2.putText(img, distancestr, (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, yawstr, (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, rollstr, (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, f'Robot heading correction: {heading_correction} {rotation_direction}', (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, f'Z1: {round(yawpitchroll_angles[0][0])} Z2:{round(yawpitchroll_angles[2][0])}', (0, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            img = draw_bounding_box(img, top_left, top_right, bottom_left, bottom_right)
            img = draw_marker_data(img, top_left, f'Roll: {rollstr}, Yaw: {yawstr}, Side: {side}, Distance: {distancestr}')
    return img, marker_list
            