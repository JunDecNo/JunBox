import json
from PySide2.QtCore import QEvent
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QPixmap
from share import *

from subWin.replace import replaceWin
from subWin.github import githubWin
from subWin.hexo import hexoWin
from subWin.maa import maaWin
from subWin.paper import paperWin

app = QApplication([])


class Main:
    def __init__(self):
        self.ui = QUiLoader().load('ui/main.ui')
        self.ui.version.setIcon(QIcon('images/version.png'))
        # 连接方法
        self.ui.version.triggered.connect(self.showVersion)

        # button
        self.ui.BtnReplace.clicked.connect(showReplace)
        self.ui.BtnGithub.clicked.connect(showGithub)
        self.ui.BtnHexo.clicked.connect(showHexo)
        self.ui.BtnMAA.clicked.connect(showMAA)
        self.ui.BtnPaper.clicked.connect(showPaper)
        self.setPixMap()


    def showVersion(self):
        QMessageBox.information(self.ui, '版本号', 'Ver 0.0.4 \n25/2/21')

    def setPixMap(self):
        self.ui.BtnReplace.setIcon(QPixmap('images/replace.png'))
        self.ui.BtnGithub.setIcon(QPixmap('images/github.png'))
        self.ui.BtnHexo.setIcon(QPixmap('images/hexo.png'))
        self.ui.BtnMAA.setIcon(QPixmap('images/maa.png'))
        self.ui.BtnPaper.setIcon(QPixmap('images/paper.png'))

    def closeEvent(self, event: QEvent):
        for window in self.sub_windows:
            window.close()
        event.accept()


app.setWindowIcon(QIcon('images/main.ico'))

SI.mainWin = Main()
SI.mainWin.ui.setWindowIcon(QIcon('images/main.ico'))

SI.replaceWin = replaceWin()
SI.replaceWin.ui.setWindowIcon(QIcon('images/replace.ico'))

SI.githubWin = githubWin()
SI.githubWin.ui.setWindowIcon(QIcon('images/github.ico'))

SI.hexoWin = hexoWin()
SI.hexoWin.ui.setWindowIcon(QIcon('images/hexo.ico'))

SI.maaWin = maaWin()
SI.maaWin.ui.setWindowIcon(QIcon('images/maa.ico'))

SI.paperWin = paperWin()
SI.paperWin.ui.setWindowIcon(QIcon('images/paper.ico'))

SI.mainWin.ui.show()
app.exec_()
