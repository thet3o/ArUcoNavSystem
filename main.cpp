#include <iostream>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui.hpp"
#include "marker/marker.h"

#define TEST true

int main() {

#if (!TEST)
    cv::VideoCapture cap(0);
#else
    cv::VideoCapture cap("../test.mp4");
#endif
    //cap.open("test.mp4");
    //int width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    //int height = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    //int fps = cap.get(cv::CAP_PROP_FPS);
    //cv::VideoWriter vwr("out0.avi", cv::VideoWriter::fourcc('h', '2', '6', '4'), fps, cv::Size(width, height));
    Marker marker("../calibration_data.xml");

    if(!cap.isOpened()){
        std::cerr << "Unable to open camera." << std::endl;
    }

    cv::Mat frame;

    while(true){
        cap>>frame;
        //cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
        Marker::Data data = marker.detect_marker(frame);

        //vwr.write(data.frame);
        cv::imshow("Test", frame);

        if (cv::waitKey(30) >= 0){ break;}
    }

    cap.release();
    //vwr.release();
    cv::destroyAllWindows();

    return 0;
}
