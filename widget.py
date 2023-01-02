
from PyQt5.QtWidgets import QApplication

from widget import Widget
from widget import Bubble

if __name__ == '__main__':
    app = QApplication([])

    bubble = Bubble()
    bubble.hide()
    widget = Widget(bubble)
    widget.show()
    
    app.exec_()
