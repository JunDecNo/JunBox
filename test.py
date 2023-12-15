from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide2.QtCore import Qt
from PySide2.QtGui import QDropEvent

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit(self)
        self.text_edit.setAcceptDrops(True)
        self.setCentralWidget(self.text_edit)

    def dragEnterEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.text_edit.setPlainText("\n".join(file_paths))

if __name__ == '__main__':
    app = QApplication([])
    main_window = MyMainWindow()
    main_window.show()
    app.exec_()
