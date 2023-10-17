import sys
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
        loadUi("main.ui", self)

        # Initialize the camera.
        self.cap = cv2.VideoCapture(0)

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

            # TODO:
            # Add detection of veins here.
            # Camera must be able to see the veins clearly for creating the dataset in the proto casing.

            self.display_image(enhanced)

    def handle_reset_button(self):
        """Handle the event when the reset button is clicked."""
        print("Reset button clicked")
        self.is_captured = False
        self.captured_frame = None
        self.timer.start(30)  # Resume updating the frames
        self.info_label.setText("Capturing in progress....")

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

    # pylint: disable=invalid-name
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
