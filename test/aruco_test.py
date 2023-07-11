import unittest
import cv2
import aruco

class ArUcoTest(unittest.TestCase):
    
    def __init__(self, methodName: str = "runTest") -> None:
        fs = cv2.FileStorage('calibration_data.xml', cv2.FILE_STORAGE_READ)
        self.mtx = fs.getNode('camera_matrix').mat()
        self.dist = fs.getNode('dist_coeffs').mat()
        fs.release()
        self.img = cv2.imread('images/one.jpg')
        self.w = self.img.shape[0]
        self.h = self.img.shape[1]
        super().__init__(methodName)
    
    def test_detection(self):
        self.assertTrue(aruco.detect_marker(self.img, self.mtx, self.dist, self.w, self.h))