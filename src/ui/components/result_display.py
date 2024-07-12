from PyQt6.QtWidgets import QTextEdit

class ResultDisplay(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def display_results(self, results):
        self.clear()
        for item in results:
            if item['type'] == 'folder':
                self.append(f"Folder: {item['path']}")
            else:
                self.append(f"File: {item['path']}")
                self.append(f"Content:\n{item['content']}\n")