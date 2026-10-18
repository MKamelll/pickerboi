import emojis
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QClipboard, QCursor, QFont, QGuiApplication, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
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
        all_emojis = {}
        print(emojis.db.get_categories())
        categories_prec = {
            "Smileys & Emotion": 1,
            "People & Body": 2,
            "Animals & Nature": 3,
            "Food & Drink": 4,
            "Objects": 5,
            "Symbols": 6,
            "Activities": 7,
            "Travel & Places": 8,
            "Flags": 9,
        }
        for c in emojis.db.get_categories():
            if categories_prec[c] not in all_emojis:
                all_emojis[categories_prec[c]] = []
            for e in emojis.db.get_emojis_by_category(c):
                all_emojis[categories_prec[c]].append(e)

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

        sorted_emojis = dict(sorted(all_emojis.items()))
        for es in sorted_emojis.values():
            for e in es:
                item = QListWidgetItem(e.emoji)
                item.setFont(QFont("Noto Color Emoji", 20))
                item.setSizeHint(QSize(50, 50))
                if len(e.aliases) > 0:
                    item.setToolTip(e.aliases[0])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setData(Qt.ItemDataRole.UserRole, " ".join(e.tags + e.aliases))
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
            emoji_tags = item.data(Qt.ItemDataRole.UserRole) or ""
            if not search_term or search_term in emoji_tags:
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
