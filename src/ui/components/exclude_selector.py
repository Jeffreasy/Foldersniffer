from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

class ExcludeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        self.exclude_files_label = QLabel("Exclude Files:")
        self.exclude_files_input = QLineEdit()
        self.exclude_dirs_label = QLabel("Exclude Directories:")
        self.exclude_dirs_input = QLineEdit()

        self.layout.addWidget(self.exclude_files_label)
        self.layout.addWidget(self.exclude_files_input)
        self.layout.addWidget(self.exclude_dirs_label)
        self.layout.addWidget(self.exclude_dirs_input)

        self.setLayout(self.layout)

    def get_exclude_files(self):
        return self.exclude_files_input.text().split(',')

    def get_exclude_dirs(self):
        return self.exclude_dirs_input.text().split(',')
