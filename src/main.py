import sys
import os

# Zorg ervoor dat 'src' aan de PYTHONPATH wordt toegevoegd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.main_window import FolderSnifferUI

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mainWin = FolderSnifferUI()
    mainWin.show()
    sys.exit(app.exec())
