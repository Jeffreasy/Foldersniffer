from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt6.QtCore import Qt
import json
import zipfile
import os

class ResultsDialog(QDialog):
    def __init__(self, results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scan Results")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.init_results_tab(results)
        self.init_edit_tab()

    def init_results_tab(self, results):
        self.results_tab = QWidget()
        self.tab_widget.addTab(self.results_tab, "Results")

        results_layout = QVBoxLayout()
        self.results_tab.setLayout(results_layout)

        self.results_tree = QTreeWidget()
        self.results_tree.setColumnCount(3)
        self.results_tree.setHeaderLabels(["File Path", "Size", "Last Modified"])
        results_layout.addWidget(self.results_tree)

        self.load_results(results)

    def load_results(self, results):
        self.results_tree.clear()  # Voeg deze regel toe om duplicaten te vermijden
        root_items = {}
        for result in results:
            path_parts = result.get("path", "").split(os.sep)
            current_item = self.results_tree
            for part in path_parts:
                if current_item == self.results_tree:
                    if part not in root_items:
                        item = QTreeWidgetItem([part])
                        self.results_tree.addTopLevelItem(item)
                        root_items[part] = item
                    current_item = root_items[part]
                else:
                    child_items = {child.text(0): child for child in [current_item.child(i) for i in range(current_item.childCount())]}
                    if part not in child_items:
                        item = QTreeWidgetItem([part])
                        current_item.addChild(item)
                        child_items[part] = item
                    current_item = child_items[part]

            current_item.setText(1, str(result.get("size", "")))
            current_item.setText(2, result.get("last_modified", ""))

    def init_edit_tab(self):
        self.edit_tab = QWidget()
        self.tab_widget.addTab(self.edit_tab, "Edit")

        edit_layout = QVBoxLayout()
        self.edit_tab.setLayout(edit_layout)

        self.edit_label = QLabel("Edit Results:")
        edit_layout.addWidget(self.edit_label)

        self.edit_input = QLineEdit()
        edit_layout.addWidget(self.edit_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_changes)
        edit_layout.addWidget(self.save_button)

        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        edit_layout.addWidget(self.export_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        edit_layout.addWidget(self.close_button)

    def save_changes(self):
        edited_text = self.edit_input.text()
        new_item = QTreeWidgetItem([edited_text])
        self.results_tree.addTopLevelItem(new_item)

    def export_results(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "JSON Files (*.json);;Text Files (*.txt);;Zip Files (*.zip)", options=options)
        if file_name:
            if file_name.endswith('.json'):
                self.save_as_json(file_name)
            elif file_name.endswith('.txt'):
                self.save_as_txt(file_name)
            elif file_name.endswith('.zip'):
                self.save_as_zip(file_name)

    def save_as_json(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.results, file)

    def save_as_txt(self, file_name):
        with open(file_name, 'w') as file:
            for result in self.results:
                file.write(f"Path: {result.get('path', '')}\n")
                file.write(f"Size: {result.get('size', '')}\n")
                file.write(f"Last Modified: {result.get('last_modified', '')}\n")
                file.write(f"Created: {result.get('created', '')}\n")
                file.write(f"Mode: {result.get('mode', '')}\n")
                file.write(f"Owner: {result.get('owner', '')}\n\n")

    def save_as_zip(self, file_name):
        txt_name = file_name.replace('.zip', '.txt')
        self.save_as_txt(txt_name)
        with zipfile.ZipFile(file_name, 'w') as zipf:
            zipf.write(txt_name, os.path.basename(txt_name))
        os.remove(txt_name)
