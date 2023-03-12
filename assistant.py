
from assistant import DesktopAssistant
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app:QApplication = QApplication([])

    assistant:DesktopAssistant = DesktopAssistant()
    assistant.show()
    
    app.exec_()
