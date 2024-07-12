import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QScrollArea, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QDateTime, QTimer
from typing import List, Dict

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        sns.set(style="darkgrid")

        self.file_type_fig, self.file_type_ax = plt.subplots(figsize=(5, 3))
        self.file_type_canvas = FigureCanvas(self.file_type_fig)

        self.file_size_fig, self.file_size_ax = plt.subplots(figsize=(5, 3))
        self.file_size_canvas = FigureCanvas(self.file_size_fig)

        self.modification_timeline_fig, self.modification_timeline_ax = plt.subplots(figsize=(5, 3))
        self.modification_timeline_canvas = FigureCanvas(self.modification_timeline_fig)

        self.event_fig, self.event_ax = plt.subplots(figsize=(5, 3))
        self.event_canvas = FigureCanvas(self.event_fig)
        
        self.summary_label = QLabel()
        self.quick_actions = QPushButton("Identify Large Files")
        self.quick_actions.clicked.connect(self.show_large_files)

        self.recent_events_table = QTableWidget(0, 2)
        self.recent_events_table.setHorizontalHeaderLabels(["Event Type", "File Path"])
        self.recent_events_table.horizontalHeader().setStretchLastSection(True)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QGridLayout(content)

        content_layout.addWidget(QLabel("File Types"), 0, 0)
        content_layout.addWidget(self.file_type_canvas, 1, 0)

        content_layout.addWidget(QLabel("File Sizes"), 0, 1)
        content_layout.addWidget(self.file_size_canvas, 1, 1)

        content_layout.addWidget(QLabel("File Modification Timeline"), 2, 0)
        content_layout.addWidget(self.modification_timeline_canvas, 3, 0)

        content_layout.addWidget(QLabel("File Events"), 2, 1)
        content_layout.addWidget(self.event_canvas, 3, 1)

        content_layout.addWidget(QLabel("Recent Events"), 4, 0, 1, 2)
        content_layout.addWidget(self.recent_events_table, 5, 0, 1, 2)

        content_layout.addWidget(self.summary_label, 6, 0)
        content_layout.addWidget(self.quick_actions, 6, 1)

        scroll.setWidget(content)
        self.layout.addWidget(scroll, 0, 0)

        self.scan_results = []
        self.scan_summary = {}
        self.file_events = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_recent_events_table)
        self.timer.start(5000)

    def update_dashboard(self, scan_results: List[Dict], scan_summary: Dict):
        self.scan_results = scan_results
        self.scan_summary = scan_summary

        if self.scan_results and self.scan_summary:
            self.update_file_type_chart()
            self.update_file_size_chart()
            self.update_modification_timeline()
            self.update_event_chart()
            self.update_summary()

    def update_file_type_chart(self):
        self.file_type_ax.clear()
        file_types = self.scan_summary.get('file_types', {})
        labels = list(file_types.keys())
        sizes = list(file_types.values())
        self.file_type_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
        self.file_type_ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.file_type_ax.set_title('File Types')
        self.file_type_fig.canvas.draw()

    def update_file_size_chart(self):
        self.file_size_ax.clear()
        size_distribution = self.scan_summary.get('size_distribution', {})
        labels = list(size_distribution.keys())
        sizes = list(size_distribution.values())
        sns.barplot(x=labels, y=sizes, palette="pastel", ax=self.file_size_ax)
        self.file_size_ax.set_xlabel('File Size')
        self.file_size_ax.set_ylabel('File Count')
        self.file_size_ax.set_title('File Sizes')
        self.file_size_fig.canvas.draw()

    def update_modification_timeline(self):
        self.modification_timeline_ax.clear()
        dates = []
        for result in sorted(self.scan_results, key=lambda x: x['last_modified']):
            date = QDateTime.fromString(result['last_modified'], "ddd MMM d HH:mm:ss yyyy")
            if date.isValid():
                dates.append(date.toMSecsSinceEpoch())
        
        if dates:
            sns.histplot(dates, bins=50, kde=False, ax=self.modification_timeline_ax, color=sns.color_palette("pastel")[0])
            self.modification_timeline_ax.set_xlabel('Modification Time')
            self.modification_timeline_ax.set_ylabel('Number of Files')
            self.modification_timeline_ax.set_title('File Modification Timeline')
            self.modification_timeline_fig.canvas.draw()

    def update_event_chart(self):
        self.event_ax.clear()
        event_counts = {
            "created": 0,
            "content modified": 0,
            "metadata modified": 0,
            "permission changed": 0,
            "deleted": 0
        }

        for event in self.file_events:
            event_counts.setdefault(event['event_type'], 0)
            event_counts[event['event_type']] += 1

        labels = list(event_counts.keys())
        counts = list(event_counts.values())
        sns.barplot(x=labels, y=counts, palette="pastel", ax=self.event_ax)
        self.event_ax.set_xlabel('Event Type')
        self.event_ax.set_ylabel('Count')
        self.event_ax.set_title('File Events')
        self.event_fig.canvas.draw()

    def update_summary(self):
        summary = f"Total Files: {self.scan_summary.get('total_files', 0)}\n"
        summary += f"Total Size: {self.format_size(self.scan_summary.get('total_size', 0))}\n"
        if self.scan_results:
            last_modified = max(result['last_modified'] for result in self.scan_results)
            summary += f"Last Scan: {last_modified}"
        
        self.summary_label.setText(summary)

    def show_large_files(self):
        large_files = sorted(self.scan_results, key=lambda x: x['size'], reverse=True)[:10]
        message = "Top 10 largest files:\n\n"
        for file in large_files:
            message += f"{file['path']}: {self.format_size(file['size'])}\n"
        QMessageBox.information(self, "Large Files", message)

    def handle_file_event(self, event_type: str, file_info: dict):
        if event_type == 'modified' and file_info.get('modification_type'):
            event_type = file_info['modification_type']
        
        self.file_events.append({"event_type": event_type, "file_path": file_info['path']})
        
        if len(self.file_events) > 100:  # Limit the number of events stored
            self.file_events.pop(0)
        self.update_event_chart()

    def update_recent_events_table(self):
        self.recent_events_table.setRowCount(0)
        for event in self.file_events[-10:]:  # Show last 10 events
            row_position = self.recent_events_table.rowCount()
            self.recent_events_table.insertRow(row_position)
            self.recent_events_table.setItem(row_position, 0, QTableWidgetItem(event['event_type']))
            self.recent_events_table.setItem(row_position, 1, QTableWidgetItem(event['file_path']))

    @staticmethod
    def format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
