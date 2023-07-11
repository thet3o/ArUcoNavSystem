"""Calibration module for ArUcoNavSystem

This module is needed to calibrate the system with the used cameras.

To calibrate the camera add all images in a folder named 'calibration_images'

"""

__author__ = 'Matteo Vacalebri (thet3o)'
__version__ = '0.0.1'

import cv2
import numpy as np
import glob
from tqdm import tqdm
import pytermgui as ptg

def calibrate_camera(rows, cols, criteria = (cv2.TERM_CRITERIA_EPS+ cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)):
    count = 0
    # Object point preparation
    objpnt = np.zeros((rows*cols, 3), np.float32)
    objpnt[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)
    
    objpoints = [] # 3D Points
    imgpoints = [] # 2D Points
    
    images = glob.glob('calibration_images/in/*.jpg')
    print(f'Found {len(images)} images')
    
    for image in tqdm(images):
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        ret, corners = cv2.findChessboardCorners(gray, (rows, cols), None)
        
        if ret == True:
            objpoints.append(objpnt)

            # Refine corners
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw chessboard corners and save the image to verify that work correctly
            cv2.drawChessboardCorners(img, (rows, cols), corners2, ret)
            cv2.imwrite(f'calibration_images/out/out{count}.jpg', img)
            count += 1
            
    ret, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    # Save calibration data
    fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_WRITE)
    fs.write('camera_matrix', mtx)
    fs.write('dist_coeffs', dist)
    fs.release()
    
def capture_images(number_of_captures):
    cap = cv2.VideoCapture(1)
    print('Start capture')
    for i in range(number_of_captures):
        _, img  = cap.read()
        cv2.imwrite(f'calibration_images/in/calib{i}.jpg', img)
    print('Capture ended')

if __name__ == '__main__':
    '''
        Size of checkerboard w:200 h:150
        Number of rows:9 cols:11
    '''
    #capture_images(50)
    #calibrate_camera(3, 3)
    
    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(
                'ArUcoNavSystem Calibrator',
                ptg.Button('Capture', centered=True, onclick=manager.stop())
            )
        ).center()
        
        manager.add(window)
    
    

