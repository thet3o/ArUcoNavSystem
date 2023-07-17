//
// Created by Matteo Vacalebri on 13/07/23.
//

#ifndef ARUCONAVSYS_MARKER_H
#define ARUCONAVSYS_MARKER_H

#include <opencv2/aruco.hpp>
class Marker {

private:
    typedef struct {
        int id;
        int distance;
        int yaw;
        int roll;
    } MarkerData;

    cv::Mat yawpitchrolldecomposition(cv::Mat R);



public:
    explicit Marker(const std::string& calibrationFilePath);
    typedef struct{
        cv::Mat camera_matrix;
        cv::Mat distortion_coefficients;
    } CalibrationData;
    typedef struct {
        //MarkerData* markerList;
        std::vector<int> markerIds;
        cv::Mat frame;
    } Data;
    Marker::Data detect_marker(cv::Mat frame);


};


#endif //ARUCONAVSYS_MARKER_H
