import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import ScraperApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec())