from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QProgressBar,
                             QCheckBox, QLabel, QGridLayout, QLineEdit, QMessageBox, QFileDialog, QTextEdit, QTabWidget,
                             QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QEventLoop
from PyQt6.QtGui import QPalette, QColor
import sys
import os
import time
import seaborn as sns
from .components.directory_selector import DirectorySelector
from .components.result_display import ResultDisplay
from .components.export_buttons import ExportButtons
from .components.filetype_selector import FileTypeSelector
from .components.exclude_selector import ExcludeSelector
from .workers.scan_worker import ScanWorker
from .dialogs.settings_dialog import SettingsDialog
from src.core.search import regex_search
from src.core.folder_comparison import compare_folders, compare_file_contents
from src.core.file_monitor import FileMonitor
from src.core.encryption_detector import is_likely_encrypted
from .components.dashboard import Dashboard


class MonitorThread(QThread):
    file_changed = pyqtSignal(str, dict)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.monitor = None

    def run(self):
        self.monitor = FileMonitor(self.directory, self.handle_file_event)
        self.monitor.start()
        loop = QEventLoop()
        loop.exec()

    def handle_file_event(self, event_type, file_info):
        self.file_changed.emit(event_type, file_info)

    def stop(self):
        if self.monitor:
            self.monitor.stop()
        self.quit()
        self.wait()

class FolderSnifferUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FolderSniffer")
        self.setGeometry(100, 100, 1000, 800)
        self.scan_results = []
        self.scan_summary = {}
        self.monitor_thread = None
        self.current_theme = "dark"
        self.dashboard_tab = Dashboard()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Add theme selector
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light"])
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_selector)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        # Create tabs
        self.tabs = QTabWidget()
        self.scan_tab = QWidget()
        self.dashboard_tab = Dashboard()
        self.tabs.addTab(self.scan_tab, "Scan")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        scan_layout = QVBoxLayout()

        self.scan_dir_selector = DirectorySelector("Scan Directory")
        self.output_dir_selector = DirectorySelector("Output Directory")
        scan_layout.addWidget(self.scan_dir_selector)
        scan_layout.addWidget(self.output_dir_selector)

        self.filetype_selector = FileTypeSelector()
        scan_layout.addWidget(self.filetype_selector)

        select_buttons_layout = QHBoxLayout()
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.filetype_selector.select_all)
        self.deselect_all_button = QPushButton("Deselect All")
        self.deselect_all_button.clicked.connect(self.filetype_selector.deselect_all)
        select_buttons_layout.addWidget(self.select_all_button)
        select_buttons_layout.addWidget(self.deselect_all_button)
        scan_layout.addLayout(select_buttons_layout)

        self.exclude_selector = ExcludeSelector()
        scan_layout.addWidget(self.exclude_selector)

        # Add the log field selection checkboxes
        log_options_layout = QGridLayout()
        self.log_size_checkbox = QCheckBox("Size")
        self.log_last_modified_checkbox = QCheckBox("Last Modified")
        self.log_created_checkbox = QCheckBox("Created")
        self.log_mode_checkbox = QCheckBox("Mode")
        self.log_owner_checkbox = QCheckBox("Owner")
        self.log_content_checkbox = QCheckBox("Content")

        log_options_layout.addWidget(QLabel("Log Fields:"), 0, 0, 1, 2)
        log_options_layout.addWidget(self.log_size_checkbox, 1, 0)
        log_options_layout.addWidget(self.log_last_modified_checkbox, 1, 1)
        log_options_layout.addWidget(self.log_created_checkbox, 2, 0)
        log_options_layout.addWidget(self.log_mode_checkbox, 2, 1)
        log_options_layout.addWidget(self.log_owner_checkbox, 3, 0)
        log_options_layout.addWidget(self.log_content_checkbox, 3, 1)

        scan_layout.addLayout(log_options_layout)

        # Add regex search bar and button
        search_layout = QHBoxLayout()
        self.regex_input = QLineEdit()
        self.regex_input.setPlaceholderText("Enter regex pattern")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_regex_search)
        search_layout.addWidget(self.regex_input)
        search_layout.addWidget(self.search_button)
        scan_layout.addLayout(search_layout)

        # Add folder comparison button
        self.compare_folders_button = QPushButton("Compare Folders")
        self.compare_folders_button.clicked.connect(self.compare_folders)
        scan_layout.addWidget(self.compare_folders_button)

        # Add file monitoring and encryption detection buttons
        monitor_layout = QHBoxLayout()
        self.start_monitor_button = QPushButton("Start File Monitoring")
        self.start_monitor_button.clicked.connect(self.toggle_file_monitoring)
        self.detect_encryption_button = QPushButton("Detect Encryption")
        self.detect_encryption_button.clicked.connect(self.detect_encryption)
        monitor_layout.addWidget(self.start_monitor_button)
        monitor_layout.addWidget(self.detect_encryption_button)
        scan_layout.addLayout(monitor_layout)

        # Add text area for file monitoring logs
        self.monitor_log = QTextEdit()
        self.monitor_log.setReadOnly(True)
        scan_layout.addWidget(self.monitor_log)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scan_layout.addWidget(self.progress_bar)

        self.start_scan_button = QPushButton("Start Scan")
        self.start_scan_button.clicked.connect(self.start_scan)
        scan_layout.addWidget(self.start_scan_button)

        self.result_display = ResultDisplay()
        scan_layout.addWidget(self.result_display)

        self.export_buttons = ExportButtons()
        self.export_buttons.json_exported.connect(self.export_as_json)
        self.export_buttons.txt_exported.connect(self.export_as_txt)
        self.export_buttons.zip_exported.connect(self.export_as_zip)
        scan_layout.addWidget(self.export_buttons)

        self.scan_tab.setLayout(scan_layout)

        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.set_theme("dark")

    def set_theme(self, theme):
        self.current_theme = theme
        if theme == "dark":
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #ffffff; }
            QPushButton { background-color: #3d3d3d; border: 1px solid #5a5a5a; padding: 5px; }
            QLineEdit, QTextEdit { background-color: #3d3d3d; border: 1px solid #5a5a5a; padding: 3px; }
            QProgressBar { border: 1px solid #5a5a5a; }
            QProgressBar::chunk { background-color: #3daee9; }
            QCheckBox::indicator { width: 15px; height: 15px; }
            QCheckBox::indicator:unchecked { background-color: #3d3d3d; border: 1px solid #5a5a5a; }
            QCheckBox::indicator:checked { background-color: #3daee9; border: 1px solid #3daee9; }
        """)

    def set_light_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #f0f0f0; color: #000000; }
            QPushButton { background-color: #e0e0e0; border: 1px solid #b0b0b0; padding: 5px; }
            QLineEdit, QTextEdit { background-color: #ffffff; border: 1px solid #b0b0b0; padding: 3px; }
            QProgressBar { border: 1px solid #b0b0b0; }
            QProgressBar::chunk { background-color: #3daee9; }
            QCheckBox::indicator { width: 15px; height: 15px; }
            QCheckBox::indicator:unchecked { background-color: #ffffff; border: 1px solid #b0b0b0; }
            QCheckBox::indicator:checked { background-color: #3daee9; border: 1px solid #3daee9; }
        """)

    def change_theme(self, theme):
        self.set_theme(theme.lower())

    def start_scan(self):
        scan_directory = self.scan_dir_selector.get_directory()
        output_directory = self.output_dir_selector.get_directory()
        if not scan_directory or not output_directory:
            return

        selected_file_types = self.filetype_selector.get_selected_file_types()
        exclude_files = self.exclude_selector.get_exclude_files()
        exclude_dirs = self.exclude_selector.get_exclude_dirs()

        # Voeg het volledige pad toe aan de te excluderen mappen
        exclude_dirs = [os.path.join(scan_directory, d.strip()) for d in exclude_dirs if d.strip()]

        log_fields = {
            'size': self.log_size_checkbox.isChecked(),
            'last_modified': self.log_last_modified_checkbox.isChecked(),
            'created': self.log_created_checkbox.isChecked(),
            'mode': self.log_mode_checkbox.isChecked(),
            'owner': self.log_owner_checkbox.isChecked(),
            'content': self.log_content_checkbox.isChecked()
        }

        self.scan_worker = ScanWorker(scan_directory, exclude_files, exclude_dirs, selected_file_types, output_directory, log_fields)
        self.scan_worker.progress.connect(self.update_progress)
        self.scan_worker.results.connect(self.scan_finished)
        self.scan_worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        # Update dashboard in real-time
        if self.scan_results and self.scan_summary:
            self.dashboard_tab.update_dashboard(self.scan_results, self.scan_summary)

    def scan_finished(self, results, log_filename, scan_summary):
        self.scan_results = results
        self.scan_summary = scan_summary
        self.result_display.display_results(results)
        self.dashboard_tab.update_dashboard(results, scan_summary)
        print(f"Log file created at: {log_filename}")
        print(f"Scan summary: {scan_summary}")

    def export_as_json(self):
        from .utils.file_operations import export_as_json
        output_directory = self.output_dir_selector.get_directory()
        if output_directory:
            export_as_json(self.scan_results, output_directory)

    def export_as_txt(self):
        from .utils.file_operations import export_as_txt
        output_directory = self.output_dir_selector.get_directory()
        if output_directory:
            export_as_txt(self.scan_results, output_directory)

    def export_as_zip(self):
        from .utils.file_operations import export_as_zip
        output_directory = self.output_dir_selector.get_directory()
        if output_directory:
            export_as_zip(self.scan_results, output_directory)

    def perform_regex_search(self):
        pattern = self.regex_input.text()
        if not pattern:
            QMessageBox.warning(self, "Warning", "Please enter a regex pattern.")
            return

        directory = self.scan_dir_selector.get_directory()
        if not directory:
            QMessageBox.warning(self, "Warning", "Please select a directory to search.")
            return

        file_types = self.filetype_selector.get_selected_file_types()
        results = regex_search(directory, pattern, file_types)
        
        self.result_display.clear()
        for result in results:
            self.result_display.append(f"File: {result['path']}")
            self.result_display.append("Matches:")
            for match in result['matches']:
                self.result_display.append(f"  - {match}")
            self.result_display.append("")

    def compare_folders(self):
        dir1 = QFileDialog.getExistingDirectory(self, "Select First Folder")
        if not dir1:
            return
        dir2 = QFileDialog.getExistingDirectory(self, "Select Second Folder")
        if not dir2:
            return

        comparison = compare_folders(dir1, dir2)
        
        self.result_display.clear()
        self.result_display.append(f"Comparison of {dir1} and {dir2}:")
        self.result_display.append(f"Common files: {', '.join(comparison['common'])}")
        self.result_display.append(f"Files only in {dir1}: {', '.join(comparison['left_only'])}")
        self.result_display.append(f"Files only in {dir2}: {', '.join(comparison['right_only'])}")
        self.result_display.append(f"Different files: {', '.join(comparison['diff_files'])}")
        
        for file in comparison['diff_files']:
            file1 = os.path.join(dir1, file)
            file2 = os.path.join(dir2, file)
            diff = compare_file_contents(file1, file2)
            self.result_display.append(f"\nDifferences in {file}:")
            self.result_display.append(''.join(diff))

    def toggle_file_monitoring(self):
        if self.monitor_thread is None:
            directory = self.scan_dir_selector.get_directory()
            if not directory:
                QMessageBox.warning(self, "Warning", "Please select a directory to monitor.")
                return
            self.monitor_thread = MonitorThread(directory)
            self.monitor_thread.file_changed.connect(self.handle_file_change)
            self.monitor_thread.start()
            self.start_monitor_button.setText("Stop File Monitoring")
        else:
            self.monitor_thread.stop()
            self.monitor_thread = None
            self.start_monitor_button.setText("Start File Monitoring")

    def handle_file_change(self, event_type, file_info):
        self.monitor_log.append(f"{event_type.capitalize()}: {file_info['path']}")
        self.dashboard_tab.handle_file_event(event_type, file_info)
        # Update dashboard in real-time for file monitoring
        if self.scan_results and self.scan_summary:
            self.update_scan_results_and_summary(event_type, file_info)
            self.dashboard_tab.update_dashboard(self.scan_results, self.scan_summary)

    def update_scan_results_and_summary(self, event_type, file_info):
        if event_type == 'created':
            self.scan_results.append(file_info)
            self.scan_summary['total_files'] += 1
            self.scan_summary['total_size'] += file_info['size']
            self.scan_summary['file_types'][file_info['extension']] = self.scan_summary['file_types'].get(file_info['extension'], 0) + 1
        elif event_type in ['content modified', 'metadata modified', 'permission changed']:
            for i, result in enumerate(self.scan_results):
                if result['path'] == file_info['path']:
                    old_size = result['size']
                    self.scan_results[i] = file_info
                    self.scan_summary['total_size'] += (file_info['size'] - old_size)
                    break
        elif event_type == 'deleted':
            for i, result in enumerate(self.scan_results):
                if result['path'] == file_info['path']:
                    self.scan_summary['total_files'] -= 1
                    self.scan_summary['total_size'] -= result['size']
                    self.scan_summary['file_types'][result['extension']] -= 1
                    if self.scan_summary['file_types'][result['extension']] == 0:
                        del self.scan_summary['file_types'][result['extension']]
                    del self.scan_results[i]
                    break

    def detect_encryption(self):
        directory = self.scan_dir_selector.get_directory()
        if not directory:
            QMessageBox.warning(self, "Warning", "Please select a directory to scan for encryption.")
            return

        self.result_display.clear()
        self.result_display.append("Scanning for potentially encrypted files...")

        encrypted_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if is_likely_encrypted(file_path):
                    encrypted_files.append(file_path)
                    self.result_display.append(f"Potentially encrypted: {file_path}")

        self.result_display.append("Encryption detection completed.")
        
        # Update dashboard with encryption information
        self.dashboard_tab.update_encryption_info(encrypted_files)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderSnifferUI()
    window.show()
    sys.exit(app.exec())
