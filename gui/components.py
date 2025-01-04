from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel

class UrlInput(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Enter YouTube URL here")

class DownloadButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

class StatusLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("")
