from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout


class GIFWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search..")
        layout.addWidget(self.search_bar)
