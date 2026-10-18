import emoji
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QClipboard, QCursor, QGuiApplication, QKeyEvent, QFont
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class EmojiPickerWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.resize(300, 300)
        all_emojis = list(emoji.EMOJI_DATA.keys())
        layout = QVBoxLayout(self)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search..")
        self.search_bar.textChanged.connect(self.filter_emojis)
        self.list_widget = QListWidget()
        self.list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setMovement(QListWidget.Movement.Static)
        self.list_widget.setSpacing(5)
        self.list_widget.itemClicked.connect(self.copy_emoji_to_clipboard)

        for i, e in enumerate(all_emojis):
            item = QListWidgetItem(e)
            item.setFont(QFont("Noto Color Emoji", 20))
            item.setSizeHint(QSize(50, 50))
            item.setToolTip(emoji.demojize(e))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setData(Qt.ItemDataRole.UserRole, e)
            self.list_widget.addItem(item)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.list_widget)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.accept()
            self.close()
            return

        super().keyPressEvent(event)

    def copy_emoji_to_clipboard(self, item: QListWidgetItem):
        e = item.text()
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(e, QClipboard.Mode.Clipboard)
        self.hide()
        QApplication.processEvents()
        self.close()

    def filter_emojis(self, text: str):
        search_term = text.strip().lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            emoji_name = (
                emoji.demojize(item.data(Qt.ItemDataRole.UserRole)).strip().lower()
            )
            if not search_term or search_term in emoji_name:
                item.setHidden(False)
            else:
                item.setHidden(True)


if __name__ == "__main__":
    import sys

    app = QApplication()
    with open("style.css", "r") as f:
        app.setStyleSheet(f.read())
    w = EmojiPickerWidget()
    cursor_pos = QCursor.pos()
    w.move(cursor_pos)
    w.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    w.destroyed.connect(app.quit)
    w.show()
    sys.exit(app.exec())
