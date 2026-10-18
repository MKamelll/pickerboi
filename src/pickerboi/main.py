from EmojiPickerWidget import EmojiPickerWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QKeyEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.resize(300, 300)

        tabs_widget = QTabWidget()
        self.setCentralWidget(tabs_widget)
        emojis_widget = EmojiPickerWidget()
        tabs_widget.addTab(emojis_widget, "Emojis")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.accept()
            self.close()
            return

        super().keyPressEvent(event)


if __name__ == "__main__":
    import sys

    app = QApplication()
    with open("style.css", "r") as f:
        app.setStyleSheet(f.read())
    w = MainWindow()
    cursor_pos = QCursor.pos()
    w.move(cursor_pos)
    w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    w.destroyed.connect(app.quit)
    w.show()
    sys.exit(app.exec())
