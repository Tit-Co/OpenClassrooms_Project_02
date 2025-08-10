from PySide6.QtCore import QObject, Signal
from scraper.scraper import scraper

class Worker(QObject):
    log_signal = Signal(str)
    finished = Signal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        import builtins
        original_print = builtins.print

        def custom_print(*args, **kwargs):
            message = " ".join(map(str, args))
            self.log_signal.emit(message)
            original_print(*args, **kwargs)

        builtins.print = custom_print

        try:
            self.log_signal.emit("🚀 Starting scraping...\n")
            scraper(self.url)
            self.log_signal.emit("\n✅ Scraping completed.\n")
        except Exception as e:
            self.log_signal.emit(f"❌ Error: {str(e)}\n")
        finally:
            builtins.print = original_print
            self.finished.emit()