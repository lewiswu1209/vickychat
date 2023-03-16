
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontMetrics

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout

class TextWindow(QWidget):
    def __init__(self) -> None:
        super(TextWindow, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        font:QFont = QFont("Helvetica", 12)

        self.text_edit:QTextEdit = QTextEdit()
        self.text_edit.setFont(font)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout:QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        self.setLayout(layout)
        self.text_edit.textChanged.connect(self.adjust_size)

    def set_plain_text(self, text:str) -> None:
        self.text_edit.setPlainText(text)

    def set_html(self, text:str) -> None:
        self.text_edit.setHtml(text)

    def set_width(self, width:int):
        old_width = self.geometry().width()
        old_x = self.geometry().x()
        self.move(old_x + old_width - width, self.geometry().y())
        self.text_edit.setFixedWidth(width)
        self.setFixedWidth(self.text_edit.width() + 20)

    def show(self) -> None:
        super().show()

        font_metrics:QFontMetrics = QFontMetrics(self.text_edit.font())
        line_space:int = font_metrics.lineSpacing()
        self.text_edit_height:int = line_space + 8
        self.max_height:int = line_space * 10 + 8
        self.text_edit.setMaximumHeight(self.max_height)

        self.text_edit.setFixedWidth(300)
        self.setFixedWidth(self.text_edit.width() + 20)
        self.text_edit.setFixedHeight(self.text_edit_height)
        self.setFixedHeight(self.text_edit.height() + 20)

        self.old_pos:QPoint = self.pos()

    def move(self, pos:QPoint):
        super().move(pos)
        self.old_pos:QPoint = self.pos()

    def move(self, x:int, y:int) -> None:
        super().move(x, y)
        self.old_pos:QPoint = self.pos()

    def adjust_size(self):
        doc = self.text_edit.document()
        doc_height = int(doc.size().height())

        if doc_height > self.max_height:
            self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        elif self.text_edit.verticalScrollBarPolicy() != Qt.ScrollBarAlwaysOff:
            self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if self.height != doc_height:
            new_height = min(doc_height, self.max_height)
            self.text_edit.setFixedHeight(new_height)
            self.setFixedHeight(new_height + 20)
            self.move(self.old_pos.x(), self.old_pos.y() - new_height + self.text_edit_height)
            self.old_pos = self.pos()
            self.text_edit_height = new_height

    def set_success_style(self):
        self.setStyleSheet("border: 3px solid #B2DFB2; border-radius: 2px;")

    def set_process_style(self):
        self.setStyleSheet("border: 3px solid #add8e6; border-radius: 2px;")
