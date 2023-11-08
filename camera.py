import picamera
import time

# Initialize the PiCamera
camera = picamera.PiCamera()

try:
    # Set camera resolution (optional, adjust as needed)
    camera.resolution = (640, 480)

    # Start the preview
    camera.start_preview()

    # Display the camera feed for 10 seconds (adjust as needed)
    time.sleep(10)

finally:
    # Stop the preview and release the camera
    camera.stop_preview()
    camera.close()
