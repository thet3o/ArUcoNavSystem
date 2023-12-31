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


aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_7X7_1000)
board = cv2.aruco.CharucoBoard_create(12, 8, 1, .8, aruco_dict)
imboard = board.draw((2000,2000))
cv2.imwrite('test.jpg',imboard)

def capture_images():
    cap = cv2.VideoCapture(2)
    running = True
    counter = 0
    while running:
        _, img = cap.read()
        
        if cv2.waitKey(1) == ord('q'):
            running = False
        if cv2.waitKey(1) == ord("c"):
            cv2.imwrite(f'calibration_images/in/cal{counter}.jpg')
            
        cv2.putText(img, f'Captures: {counter}', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2, cv2.LINE_AA)
        
        cv2.imshow('Capture', img)
    
    cap.release()
    cv2.destroyAllWindows()
        

def read_charuco(images):
    print('POSE ESTIMATION STARTS:')
    all_corners = []
    all_ids = []
    decimator = 0
    
    # sub pixel corner
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
    
    for image in images:
        #img = cv2.imread(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict)
        
        if len(corners) > 0:
            # sub pixel detection
            for corner in corners:
                cv2.cornerSubPix(gray, corner, winSize=(3,3), zeroZone=(-1,-1), criteria=criteria)
                res = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
                if res[1] is not None and res[2] is not None and len(res[1])>3 and decimator%1==0:
                    all_corners.append(res[1])
                    all_ids.append(res[2])
        decimator += 1
    imsize = gray.shape
    return all_corners, all_ids, imsize

def calibrate_camera(all_corners, all_ids, imsize):
    print('Camera calibration')
    
    camera_matrix_init = np.array([[1000., 0., imsize[0]/2.],
                                   [0., 1000., imsize[1]/2.],
                                   [0., 0., 1.]])
    
    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    
    (ret, camera_matrix, distortion_coefficients, 
     rotation_vectors, translation_vectors, std_deviations_intrinsics,
     std_deviations_extrinsics, per_view_errors) = cv2.aruco.calibrateCameraCharucoExtended(
         charucoCorners = all_corners, charucoIds = all_ids, board = board,
         imageSize = imsize, cameraMatrix = camera_matrix_init, distCoeffs = distCoeffsInit,
         flags = flags, criteria = (cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9)
     )
     
    return ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors

if __name__ == '__main__':
    
    # Get images path
    images = glob.glob('calibration_images/in/*.jpg')
    print(f'Found {len(images)} images')
    
    #Calibrate camera
    all_corners, all_ids, imsize = read_charuco(images)
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(all_corners, all_ids, imsize)
    
    # Save calibration data
    fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_WRITE)
    fs.write('camera_matrix', mtx)
    fs.write('dist_coeffs', dist)
    fs.release()

