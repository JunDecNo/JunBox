import subprocess
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog


class githubWin:
    def __init__(self):
        self.ui = QUiLoader().load('ui/github.ui')
        self.ui.proxy.setPlaceholderText('https://github.moeyy.xyz/')
        self.ui.btnStart.clicked.connect(self.Download)
        self.ui.btnFile.clicked.connect(self.selectFilePath)
        # self.ui.selectFilePath.clicked.connect(self.selectFilePath)

    def Download(self):
        proxy_url = self.ui.proxy.text()
        git_url = self.ui.gitPath.text()
        save_path = self.ui.savePath.text()
        if proxy_url == '' or not proxy_url.endswith('/'):
            proxy_url = 'https://github.moeyy.xyz/'
        if git_url.endswith('.git'):
            command = f'git clone {proxy_url}{git_url} {save_path}/{git_url.split(".")[1].split("/")[-1]}'
        else:
            command = f'wget {proxy_url}{git_url} -O {save_path}/{git_url.split("/")[-1]}'
        self.ui.textBrowser.insertPlainText('开始执行\n')
        process = subprocess.run(command, shell=True)
        if process.returncode == 0:
            self.ui.textBrowser.insertPlainText(process.stdout)
            self.ui.textBrowser.insertPlainText('执行成功\n')
        else:
            self.ui.textBrowser.insertPlainText(process.stderr)
            self.ui.textBrowser.insertPlainText('执行失败\n')

    def selectFilePath(self):
        # 打开文件浏览界面
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 获取文件路径
        file_path = QFileDialog.getExistingDirectory(self.ui, "选取文件夹", "./")
        self.ui.savePath.setText(file_path)
