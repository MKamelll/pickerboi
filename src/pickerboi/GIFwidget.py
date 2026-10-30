from GiphyApi import GIF, giphy_api_instance
from PySide6.QtConcurrent import QtConcurrent
from PySide6.QtCore import (
    QBuffer,
    QByteArray,
    QObject,
    QRunnable,
    Qt,
    QThreadPool,
    QUrl,
    Signal,
    Slot,
)
from PySide6.QtGui import QMovie
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


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
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.download_finished)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.progress_bar)

    def copy_gif_to_clipboard(self):
        pass

    def load_trending(self, limit: int = 10):
        worker = Worker(giphy_api_instance.get_trending, limit=limit)
        worker.signals.started.connect(self.progress_bar.show)
        worker.signals.finished.connect(self.progress_bar.hide)
        worker.signals.finished.connect(self.details_result)
        self.threadpool.start(worker)

    def download_finished(self, reply: QNetworkReply):
        label = QLabel(self.list_widget)
        if reply.error() != reply.NetworkError.NoError:
            label.setText(f"Error loading the gif: {reply.errorString()}")
            reply.deleteLater()
            return

        raw_data = reply.readAll()
        reply.deleteLater()
        buffer = QBuffer(self.list_widget)
        buffer.setData(raw_data)
        buffer.open(QBuffer.OpenModeFlag.ReadOnly)
        gif = QMovie(buffer, QByteArray(b"GIF"))

        if gif.isValid():
            label.setMovie(gif)
            gif.start()
        else:
            label.setText("Downloaded data is not valid GIF format")

        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(label.sizeHint())
        self.list_widget.setItemWidget(item, label)

    def details_result(self, result: list[GIF]):
        for i in result:
            self.manager.get(QNetworkRequest(QUrl(i.media_url)))
