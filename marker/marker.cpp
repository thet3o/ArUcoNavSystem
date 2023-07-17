//
// Created by Matteo Vacalebri on 13/07/23.
//

#include "marker.h"
#include "opencv2/opencv.hpp"
#include "fmt/format.h"
#include <cmath>

#define markerLength 0.035

static Marker::CalibrationData calibrationData;
static cv::Mat objPoints(4, 1, CV_32FC3);

Marker::Marker(const std::string& calibrationFilePath) {

    cv::Mat camera_matrix, distortion_coefficients;

    // Load calibration data
    cv::FileStorage fileStorage(calibrationFilePath, cv::FileStorage::READ);
    fileStorage["camera_matrix"] >> camera_matrix;
    fileStorage["dist_coeffs"] >> distortion_coefficients;
    fileStorage.release();

    calibrationData = {camera_matrix, distortion_coefficients};

    // Init object points matrix
    objPoints.ptr<cv::Vec3f>(0)[0] = cv::Vec3f(-markerLength/2.f, markerLength/2.f, 0);
    objPoints.ptr<cv::Vec3f>(0)[1] = cv::Vec3f(markerLength/2.f, markerLength/2.f, 0);
    objPoints.ptr<cv::Vec3f>(0)[2] = cv::Vec3f(markerLength/2.f, -markerLength/2.f, 0);
    objPoints.ptr<cv::Vec3f>(0)[3] = cv::Vec3f(-markerLength/2.f, -markerLength/2.f, 0);
}

Marker::Data Marker::detect_marker(cv::Mat frame) {

    // Set dictionary
    cv::aruco::Dictionary dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_7X7_250);
    cv::aruco::DetectorParameters detectorParameters = cv::aruco::DetectorParameters();

    std::vector<int> markerIds;
    std::vector<std::vector<cv::Point2f>> markerCorners, rejectedCandidates;

    cv::aruco::ArucoDetector detector(dictionary, detectorParameters);

    detector.detectMarkers(frame, markerCorners, markerIds, rejectedCandidates);

    // Count markers
    unsigned int nMarkers = markerCorners.size();
    std::vector<cv::Vec3d> rvecs(nMarkers), tvecs(nMarkers);

    // Draw markers
    if(!markerIds.empty()){
        // Corner Sub Pixelation
        /*
        cornerSubPix(frame, markerCorners,
                     Size(3,3), Size(-1,-1),
                     TermCriteria(TermCriteria::EPS + TermCriteria::MAX_ITER, 100, 0.001));*/
        cv::aruco::drawDetectedMarkers(frame, markerCorners, markerIds);
    }

    // Estimate pose
    for(int i = 0; i < nMarkers; i++) {
        solvePnP(objPoints, markerCorners.at(i),
                                         calibrationData.camera_matrix,
                                         calibrationData.distortion_coefficients,
                                         rvecs.at(i), tvecs.at(i));
    }

    for(int i = 0; i < markerIds.size(); i++){
        cv::Mat rotMat;
        auto rvec = rvecs[i];
        auto tvec = tvecs[i];
        Rodrigues(rvec, rotMat);
        cv::Mat ypr = -180*yawpitchrolldecomposition(rotMat)/M_PI; // Yaw 0, Pitch 1, Roll 2
        ypr.at<double>(0, 1) += 90;
        std::cout << ypr << std::endl;
        std::string str = "Yaw:" + std::to_string(ypr.at<double>(0)) + "Pitch:" + std::to_string(ypr.at<double>(1)) + "Roll:" + std::to_string(ypr.at<double>(2));
        putText(frame, str, cv::Point(50, 100),
                cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 255, 0), 2, false);
        drawFrameAxes(frame, calibrationData.camera_matrix, calibrationData.distortion_coefficients, rvec, tvec,
                      0.1);
    }

    return {markerIds, frame};
}


cv::Mat Marker::yawpitchrolldecomposition(cv::Mat R) {
    cv::Mat expr = R.row(2).col(0) * R.row(2).col(0) + R.row(2).col(1) * R.row(2).col(1);
    double sin_x = std::sqrt(expr.at<double>(0,0));
    bool validity = sin_x < 1e-6;
    double z1, x, z2;
    if(!validity){
        z1 = std::atan2(R.at<double>(2,0), R.at<double>(2,1));
        x = std::atan2(sin_x, R.at<double>(2,2));
        z2 = std::atan2(R.at<double>(0,2), -R.at<double>(1,2));
    }else{
        z1 = 0;
        x = std::atan2(sin_x, R.at<double>(2,2));
        z2 = 0;
    }

    cv::Mat res(1,3, CV_64F);
    res.at<double>(0,0) = z1;
    res.at<double>(0,1) = x;
    res.at<double>(0,2) = z2;

    return res;
}
