#include <iostream>
#include <libcamera/camera_manager.h>
#include <opencv2/opencv.hpp>

int main() {
    libcamera::CameraManager manager;
    manager.start();

    const std::vector<libcamera::Camera*> cameras = manager.cameras();

    if (cameras.empty()) {
        std::cerr << "No cameras found." << std::endl;
        return 1;
    }

    libcamera::Camera* camera = cameras[0];

    if (camera->acquire()) {
        std::cerr << "Failed to acquire the camera." << std::endl;
        return 1;
    }

    camera->configure();

    cv::VideoCapture capture(camera->name());
    if (!capture.isOpened()) {
        std::cerr << "Failed to open camera." << std::endl;
        return 1;
    }

    cv::Mat frame;

    while (true) {
        capture >> frame;

        if (frame.empty()) {
            break;
        }

        cv::imshow("Camera Feed", frame);
        char key = cv::waitKey(10);

        if (key == 27) {
            break;  // Exit the loop when the 'ESC' key is pressed.
        }
    }

    capture.release();
    cv::destroyAllWindows();
    camera->release();

    return 0;
}
