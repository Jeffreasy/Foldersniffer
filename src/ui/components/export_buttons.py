from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal

class ExportButtons(QWidget):
    json_exported = pyqtSignal()
    txt_exported = pyqtSignal()
    zip_exported = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        self.json_button = QPushButton("Export as JSON")
        self.json_button.clicked.connect(self.export_json)
        self.layout.addWidget(self.json_button)

        self.txt_button = QPushButton("Export as TXT")
        self.txt_button.clicked.connect(self.export_txt)
        self.layout.addWidget(self.txt_button)

        self.zip_button = QPushButton("Export as ZIP")
        self.zip_button.clicked.connect(self.export_zip)
        self.layout.addWidget(self.zip_button)

        self.setLayout(self.layout)

    def export_json(self):
        self.json_exported.emit()

    def export_txt(self):
        self.txt_exported.emit()

    def export_zip(self):
        self.zip_exported.emit()
