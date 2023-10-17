import sys
import os
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for GUI related controls in main.ui.
    """

    def __init__(self):
        """Initialize the main window, camera, and UI event handlers."""
        super(MainWindow, self).__init__()

        # Get the directory of the current script.
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Join it with the file name to get its absolute path.
        ui_file_path = os.path.join(script_dir, "main.ui")

        loadUi(ui_file_path, self)

        self.showFullScreen()

        # Initialize the camera
        # For PC
        # self.cap = cv2.VideoCapture(0)

        # For Jetson Nano
        self.cap = cv2.VideoCapture(
            "nvarguscamerasrc ! nvvidconv ! video/x-raw, width=1024, height=576, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink",
            cv2.CAP_GSTREAMER,
        )

        # Initialize the timer for receiving frames from the camera.
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)  # Update roughly 30 times per second.

        # Initialize the event handlers for the UI elements.
        self.init_ui_event_handlers()

        # Flags and storage variables
        self.is_captured = False
        self.captured_frame = None

        # Set initial info label text
        self.info_label.setText("Capturing in progress....")

    def init_ui_event_handlers(self):
        """
        Initialize the event handlers for the UI elements.
        """
        self.capture_button.clicked.connect(self.handle_capture_button)
        self.identify_button.clicked.connect(self.handle_identify_button)
        self.reset_button.clicked.connect(self.handle_reset_button)

    def handle_capture_button(self):
        """Handle the event when the capture button is clicked."""
        print("Capture button clicked")
        ret, self.captured_frame = self.cap.read()

        if not ret:
            self.captured_frame = None
        self.timer.stop()  # Stop updating the frames
        self.is_captured = True
        self.info_label.setText(
            "Image captured. Press <b>Identify</b> to detect or press <b>Reset</b> to resume camera."
        )
        self.result_input.setText("")

    def handle_identify_button(self):
        """Handle the event when the identify button is clicked."""
        print("Identify button clicked")
        if not self.is_captured:
            self.info_label.setText(
                "Click <b>Capture</b> image first before clicking <b>Identify</b>"
            )
            return

        if self.captured_frame is not None:
            # Convert the image to grayscale
            gray = cv2.cvtColor(self.captured_frame, cv2.COLOR_BGR2GRAY)

            # Gaussian blur to remove noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Use CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(blurred)

            # Extract region of interest (ROI)
            x, y, w, h = 420, 220, 100, 100  # Example coordinates for the region
            roi = enhanced[y : y + h, x : x + w]

            # Check if the ROI is a valid vein region (not too bright or too dark)
            if not self.is_valid_vein_region(roi):
                self.result_input.setText("No Vein Detected")
            else:
                self.result_input.setText("Vein Detected")

            # Draw the rectangle around the ROI on the enhanced image
            # color = (0, 255, 0)  # Green color
            # thickness = 2
            # cv2.rectangle(enhanced, (x, y), (x + w, y + h), color, thickness)

            self.display_image(enhanced)

    def is_valid_vein_region(self, region):
        """Check if a given region is a valid vein region (not too bright)."""
        bright_threshold = 200  # Adjust this value based on your needs
        mean_brightness = region.mean()

        if mean_brightness > bright_threshold:
            return False
        return True

    def handle_reset_button(self):
        """Handle the event when the reset button is clicked."""
        print("Reset button clicked")
        self.is_captured = False
        self.captured_frame = None
        self.timer.start(30)  # Resume updating the frames
        self.info_label.setText("Capturing in progress....")
        self.result_input.setText("")

    def display_image(self, frame):
        """Utility function to display an image on the QLabel."""
        if len(frame.shape) == 2:  # Check if the frame is grayscale
            height, width = frame.shape
            bytes_per_line = 1 * width
            image_format = QtGui.QImage.Format_Grayscale8
            out_image = QtGui.QImage(
                frame.data, width, height, bytes_per_line, image_format
            )
        else:  # If the frame is RGB
            height, width, _ = frame.shape
            bytes_per_line = 3 * width
            image_format = QtGui.QImage.Format_RGB888
            out_image = QtGui.QImage(
                frame.data, width, height, bytes_per_line, image_format
            )

        self.image_label.setPixmap(QtGui.QPixmap.fromImage(out_image))
        self.image_label.setScaledContents(True)

    def update_frames(self):
        """
        Timer callback that continuously retrieves and displays frames from the camera.
        """
        ret, frame = self.cap.read()
        if not ret:
            return

        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.display_image(frame)

    def closeEvent(self, event):
        """Release the camera when the window is closed."""
        if hasattr(self, "cap") and self.cap.isOpened():
            self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
