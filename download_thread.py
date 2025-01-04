from PySide6.QtCore import QThread, Signal
from core.downloader import download_video

class DownloadThread(QThread):
    progress = Signal(float)
    finished = Signal()

    def __init__(self, url, quality, folder):
        super().__init__()
        self.url = url
        self.quality = quality
        self.folder = folder

    def run(self):
        # Start the download and pass the update progress callback
        download_video(self.url, self.quality, self.folder, self.update_progress)
        self.finished.emit()
        

    def update_progress(self, percent):
        self.progress.emit(percent)

