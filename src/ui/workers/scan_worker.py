from PyQt6.QtCore import QThread, pyqtSignal
from src.core.scanner import scan_directory

class ScanWorker(QThread):
    progress = pyqtSignal(int)
    results = pyqtSignal(list, str, dict)  # Aangepast om ook scan_summary te verzenden

    def __init__(self, directory, ignore_files, ignore_dirs, file_types, output_directory, log_fields):
        super().__init__()
        self.directory = directory
        self.ignore_files = ignore_files
        self.ignore_dirs = ignore_dirs
        self.file_types = file_types
        self.output_directory = output_directory
        self.log_fields = log_fields

    def run(self):
        log_filename, result_list, scan_summary = scan_directory(
            self.directory,
            self.output_directory,
            self.log_fields,
            self.ignore_files,
            self.ignore_dirs,
            self.file_types,
            progress_callback=self.progress.emit
        )
        self.results.emit(result_list, log_filename, scan_summary)