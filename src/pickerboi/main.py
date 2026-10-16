import emoji
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QKeyEvent, QGuiApplication, QClipboard
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)


class EmojiPickerWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.resize(300, 300)
        all_emojis = list(emoji.EMOJI_DATA.keys())
        layout = QVBoxLayout(self)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search..")
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        container_layout = QGridLayout(container)
        container_layout.setSpacing(4)

        max_cols = 5

        for i, e in enumerate(all_emojis):
            row = i // max_cols
            col = i % max_cols
            btn = QPushButton(e)
            btn.clicked.connect(
                lambda checked=False, e=e: self.copy_emoji_to_clipboard(e)
            )
            btn.setFixedSize(45, 45)
            container_layout.addWidget(btn, row, col)

        scroll.setWidget(container)
        layout.addWidget(search_bar)
        layout.addWidget(scroll)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.accept()
            self.close()
            return

        super().keyPressEvent(event)

    def copy_emoji_to_clipboard(self, e: str):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(e, QClipboard.Mode.Clipboard)
        self.hide()
        QApplication.processEvents()
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication()
    w = EmojiPickerWidget()
    cursor_pos = QCursor.pos()
    w.move(cursor_pos)
    w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    w.destroyed.connect(app.quit)
    w.show()
    sys.exit(app.exec())
