from PyQt6.QtWidgets import (QWidget, QGridLayout, QCheckBox, QPushButton, QScrollArea, 
                             QHBoxLayout, QDialog, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class FileTypeSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)

        self.file_types = [
            ("py", "Python source code"),
            ("java", "Java source code"),
            ("cpp", "C++ source code"),
            ("c", "C source code"),
            ("cs", "C# source code"),
            ("html", "HTML file"),
            ("css", "Cascading Style Sheets"),
            ("js", "JavaScript source code"),
            ("ts", "TypeScript source code"),
            ("json", "JSON data file"),
            ("xml", "XML data file"),
            ("md", "Markdown document"),
            ("csv", "Comma-separated values file"),
            ("tsv", "Tab-separated values file"),
            ("yaml", "YAML data file"),
            ("yml", "YAML data file"),
            ("ini", "Configuration file"),
            ("log", "Log file"),
            ("sql", "SQL database file"),
            ("sh", "Shell script"),
            ("bat", "Windows batch file"),
            ("r", "R programming language"),
            ("rb", "Ruby source code"),
            ("swift", "Swift source code"),
            ("kt", "Kotlin source code"),
            ("go", "Go source code"),
            ("pl", "Perl source code"),
            ("php", "PHP source code"),
            ("asp", "Active Server Pages"),
            ("aspx", "ASP.NET Web Forms"),
            ("jsp", "JavaServer Pages"),
            ("dart", "Dart source code"),
            ("scala", "Scala source code"),
            ("erl", "Erlang source code"),
            ("ex", "Elixir source code"),
            ("exs", "Elixir script"),
            ("hs", "Haskell source code"),
            ("lhs", "Literate Haskell source code"),
            ("rs", "Rust source code"),
            ("jl", "Julia source code"),
            ("m", "MATLAB source code"),
            ("mat", "MATLAB data file"),
            ("groovy", "Groovy source code"),
            ("lua", "Lua source code"),
            ("rkt", "Racket source code"),
            ("rktl", "Racket source code"),
            ("v", "Verilog source code"),
            ("sv", "SystemVerilog source code"),
            ("svh", "SystemVerilog header"),
            ("sby", "SymbiYosys script"),
            ("awk", "AWK script"),
            ("cmd", "Windows Command script"),
            ("vbs", "VBScript source code"),
            ("tsx", "TypeScript React file")
        ]

        self.checkboxes = []
        for i, (file_type, description) in enumerate(self.file_types):
            checkbox = QCheckBox(file_type)
            checkbox.setToolTip(description)
            checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.checkboxes.append(checkbox)
            scroll_layout.addWidget(checkbox, i // 4, i % 4)  # 4 columns grid

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        self.layout.addWidget(scroll)

        self.setLayout(self.layout)

    def select_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def deselect_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def get_selected_file_types(self):
        return [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

class FileTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select File Types")
        self.setGeometry(200, 200, 400, 500)

        self.layout = QVBoxLayout()

        self.file_type_selector = FileTypeSelector(self)
        self.layout.addWidget(self.file_type_selector)

        # Select all / Deselect all buttons
        btn_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.file_type_selector.select_all)
        btn_layout.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.file_type_selector.deselect_all)
        btn_layout.addWidget(deselect_all_btn)

        self.layout.addLayout(btn_layout)

        # OK and Cancel buttons
        action_btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        action_btn_layout.addWidget(ok_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        action_btn_layout.addWidget(cancel_btn)

        self.layout.addLayout(action_btn_layout)

        self.setLayout(self.layout)

    def get_selected_file_types(self):
        return self.file_type_selector.get_selected_file_types()