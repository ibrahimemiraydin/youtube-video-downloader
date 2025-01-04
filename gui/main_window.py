import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QLineEdit, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QThread, Signal
from download_thread import DownloadThread
import subprocess


class ConvertThread(QThread):
    progress = Signal(int)  # Signal to update progress
    finished = Signal(str)  # Signal to indicate conversion is finished

    def __init__(self, file_path, ffmpeg_path):
        super().__init__()
        self.file_path = file_path
        self.ffmpeg_path = ffmpeg_path

    def run(self):
        output_file = os.path.splitext(self.file_path)[0] + "_converted.mp4"
        ffmpeg_command = [
            self.ffmpeg_path,
            '-i', self.file_path,
            '-c:v', 'h264_nvenc',
            '-c:a', 'aac',
            '-preset', 'fast',
            output_file
        ]

        try:
            # Run the conversion process
            subprocess.run(ffmpeg_command, check=True)
            self.finished.emit(f"Conversion complete: {output_file}")
        except subprocess.CalledProcessError as e:
            self.finished.emit(f"Error during conversion: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the application icon
        icon_path = os.path.join(os.path.dirname(__file__), '../resources/icons/app_icon.ico')  # Path to your icon file
        self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(300, 300, 650, 550)

        # Set the path to ffmpeg
        self.ffmpeg_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', 'core', 'ffmpeg', 'bin', 'ffmpeg.exe'
        )
        self.ffmpeg_path = os.path.abspath(self.ffmpeg_path)

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title Label (centered)
        self.title_label = QLabel("YouTube Video Downloader")
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold; color: #5A9BFF; margin-bottom: 20px; text-align: center;")

        # URL Input Section
        self.url_label = QLabel("Enter YouTube URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL here")
        self.url_input.setStyleSheet("background-color: #2C2C2C; color: white; padding: 10px; border-radius: 5px; font-size: 16px;")

        # Quality Selection
        self.quality_label = QLabel("Select Quality:")
        self.quality_dropdown = QComboBox()
        self.quality_dropdown.addItems(["Highest Quality", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p", "Audio Only"])
        self.quality_dropdown.setStyleSheet("background-color: #2C2C2C; color: white; padding: 10px; border-radius: 5px; font-size: 16px;")

        # Folder Selection
        self.folder_label = QLabel("Select Destination Folder:")
        self.folder_button = QPushButton("Browse...")
        self.folder_button.clicked.connect(self.select_folder)
        self.folder_button.setStyleSheet("""background-color: #5A9BFF; color: white; padding: 10px; border-radius: 5px; font-size: 16px;""")

        self.destination_folder = QLineEdit()
        self.destination_folder.setPlaceholderText("No folder selected")
        self.destination_folder.setReadOnly(True)
        self.destination_folder.setStyleSheet("background-color: #2C2C2C; color: #A3A3A3; padding: 10px; border-radius: 5px; font-size: 16px;")

        # Download Button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.handle_download)
        self.download_button.setStyleSheet("""background-color: #5A9BFF; color: white; padding: 15px; border-radius: 5px; font-size: 18px;""")
        self.download_button.setFixedHeight(50)

        # Convert Button
        self.convert_button = QPushButton("Convert to MP4 (H.264 + AAC)")
        self.convert_button.clicked.connect(self.handle_convert)
        self.convert_button.setStyleSheet("""background-color: #5A9BFF; color: white; padding: 15px; border-radius: 5px; font-size: 18px;""")
        self.convert_button.setFixedHeight(50)

        # Status Label (centered notifications)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #A3A3A3; font-size: 16px; text-align: center; margin-top: 20px;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Layout Setup
        url_quality_layout = QVBoxLayout()
        url_quality_layout.addWidget(self.url_label)
        url_quality_layout.addWidget(self.url_input)
        url_quality_layout.addWidget(self.quality_label)
        url_quality_layout.addWidget(self.quality_dropdown)

        folder_layout = QVBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_button)
        folder_layout.addWidget(self.destination_folder)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.download_button)
        buttons_layout.addWidget(self.convert_button)

        progress_layout = QVBoxLayout()
        progress_layout.addWidget(self.status_label)

        # Main Layout
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)  # Ensures title is centered
        main_layout.addLayout(url_quality_layout)
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(progress_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply the custom stylesheet from the external QSS file
        self.load_styles()

    def load_styles(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), '../resources/styles.qss'), 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error loading QSS file: {e}")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.destination_folder.setText(folder)

    def handle_download(self):
        url = self.url_input.text()
        quality = self.quality_dropdown.currentText()
        folder = self.destination_folder.text()

        if not url:
            self.status_label.setText("Please enter a valid URL.")
            return
        if not folder:
            self.status_label.setText("Please select a destination folder.")
            return

        self.status_label.setText("Downloading...")

        # Start the download in a separate thread
        self.download_thread = DownloadThread(url, quality, folder)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, percent):
        percent_str = f"{percent:.1f}".lstrip("94")
        self.status_label.setText(f"Downloading... {percent_str}%")  # Update status label with cleaned percentage

    def download_finished(self):
        self.status_label.setText("Download complete!")

    def handle_convert(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.mkv *.avi *.mov)")

        if file_path:
            # Inform the user that the process may take a while
            self.status_label.setText("Converting video... This process may take a long time.")

            # Create and start the conversion thread
            self.convert_thread = ConvertThread(file_path, self.ffmpeg_path)
            self.convert_thread.progress.connect(self.update_progress)  # You can also track progress here if needed
            self.convert_thread.finished.connect(self.convert_finished)
            self.convert_thread.start()

    def convert_finished(self, message):
        self.status_label.setText(message)
