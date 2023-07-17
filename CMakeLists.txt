cmake_minimum_required(VERSION 3.26)
project(ArUcoNavSys)

set(CMAKE_CXX_STANDARD 17)

set(OpenCV_DIR "${VCPKG_INSTALLED_DIR}/arm64-osx/share/opencv4")
find_package(OpenCV REQUIRED)

add_executable(ArUcoNavSys main.cpp
        marker/marker.cpp
        marker/marker.h
        path_finding/path_finder.cpp
        path_finding/path_finder.h)
target_link_libraries(ArUcoNavSys ${OpenCV_LIBS})