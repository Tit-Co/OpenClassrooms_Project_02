import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import Signal, QObject, QThread
from scraper.config import index_url
from .worker import Worker

class EmittingStream(QObject):
    text_written = Signal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass

class ScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraper GUI")
        self.resize(1024, 768)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        btn = QPushButton("Start/Stop scraping")

        layout = QVBoxLayout()
        layout.addWidget(self.log)
        layout.addWidget(btn)
        self.setLayout(layout)

        # redirect print()
        self.emitter = EmittingStream()

        btn.clicked.connect(self.run_scraping)

    def run_scraping(self):

        # Creation of thread and worker
        self.thread = QThread()
        self.worker = Worker(index_url)
        self.worker.moveToThread(self.thread)

        # Connctions signals
        self.thread.started.connect(self.worker.run)
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    def append_log(self, message):
        self.log.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec())