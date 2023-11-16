from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QPixmap
from share import SI
from subWin.replace import replaceWin

app = QApplication([])


class Main:
    def __init__(self):
        self.ui = QUiLoader().load('ui/main.ui')
        self.ui.version.setIcon(QIcon('images/version.png'))
        # 连接方法
        self.ui.version.triggered.connect(self.showVersion)
        self.ui.BtnReplace.clicked.connect(self.showReplace)
        self.setPixMap()

    def showVersion(self):
        QMessageBox.information(self.ui, '版本号', 'Ver 0.0.1 \n23/11/15')

    def showReplace(self):
        SI.replaceWin.ui.show()

    def setPixMap(self):
        self.ui.BtnReplace.setIcon(QPixmap('images/replace.png'))


app.setWindowIcon(QIcon('images/main.ico'))
SI.mainWin = Main()
SI.replaceWin = replaceWin()
SI.replaceWin.ui.setWindowIcon(QIcon('images/replace.ico'))
SI.mainWin.ui.show()
app.exec_()
