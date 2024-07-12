from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

class DirectorySelector(QWidget):
    def __init__(self, label_text):
        super().__init__()
        self.init_ui(label_text)

    def init_ui(self, label_text):
        layout = QHBoxLayout()
        self.label = QLabel(label_text)
        self.input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_directory)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.browse_button)

        self.setLayout(layout)

    def select_directory(self):
        try:
            directory = QFileDialog.getExistingDirectory(self, f"Select {self.label.text()}")
            if directory:
                self.input.setText(directory)
        except Exception as e:
            print(f"Error selecting directory: {e}")

    def get_directory(self):
        return self.input.text()