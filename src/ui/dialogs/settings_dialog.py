from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Example setting: Default Directory
        self.default_dir_label = QLabel("Default Directory:")
        layout.addWidget(self.default_dir_label)

        self.default_dir_input = QLineEdit()
        layout.addWidget(self.default_dir_input)

        # Save Button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def save_settings(self):
        # Logic to save settings
        pass
