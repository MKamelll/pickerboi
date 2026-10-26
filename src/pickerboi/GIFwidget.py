from GiphyApi import giphy_api_instance
from PySide6.QtConcurrent import QtConcurrent
from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QLineEdit, QListWidget, QProgressBar, QVBoxLayout, QWidget


class WorkerSignals(QObject):
    started = Signal()
    finished = Signal(object)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        self.signals.started.emit()
        result = self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit(result)


class GIFWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search..")
        self.list_widget = QListWidget()
        self.list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setMovement(QListWidget.Movement.Static)
        self.list_widget.setSpacing(5)
        self.list_widget.itemClicked.connect(self.copy_gif_to_clipboard)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        self.threadpool = QThreadPool.globalInstance()

        layout.addWidget(self.search_bar)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.progress_bar)

    def copy_gif_to_clipboard(self):
        pass

    def load_trending(self, limit: int = 10):
        worker = Worker(giphy_api_instance.get_trending, limit=limit)
        worker.signals.started.connect(self.progress_bar.show)
        worker.signals.finished.connect(self.progress_bar.hide)
        worker.signals.finished.connect(self.handle_result)
        self.threadpool.start(worker)

    def handle_result(self, result):
        print(result)
