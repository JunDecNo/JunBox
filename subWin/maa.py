import json
import os
import shutil
import zipfile
import requests
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog, QMessageBox
from utils import *


class maaWin:

    def __init__(self):
        self.ui = QUiLoader().load('ui/maa.ui')
        self.ui.btnStart.clicked.connect(self.Update)
        self.ui.btnFile.clicked.connect(self.selectFilePath)
        self.jsonData = json.load(open(getRootPath() + '/subWin/config.json', 'r', encoding='utf-8'))

    def Update(self):
        git_url = 'https://github.com/MaaAssistantArknights/MaaResource/archive/main.zip'
        maa_path = self.ui.savePath.text()
        if maa_path == '':
            maa_path = self.jsonData['maa_path']

        thread = threading.Thread(target=self.download, args=(maa_path, git_url)) # 多进程，防止未响应
        thread.start()

    def selectFilePath(self):
        # 打开文件浏览界面
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 获取文件路径
        file_path = QFileDialog.getExistingDirectory(self.ui, "选取文件夹", "./")
        self.ui.savePath.setText(file_path)

    def download(self, save_path, repo_url):
        try:
            if repo_url == None:
                repo_url = 'https://github.com/MaaAssistantArknights/MaaResource/archive/main.zip'
            response = requests.get(repo_url)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                self.ui.textBrowser.insertPlainText(f"Repository downloaded successfully to {save_path}")
            else:
                self.ui.textBrowser.insertPlainText(f"Failed to download repository. Status code: {response.status_code}")
        except:
            # 开启代理
            proxy = 'http://127.0.0.1:10808'
            response = requests.get(repo_url, proxies={'http': proxy, 'https': proxy})
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                self.ui.textBrowser.insertPlainText(f"Repository downloaded successfully to {save_path}")
            else:
                self.ui.textBrowser.insertPlainText(f"Failed to download repository. Status code: {response.status_code}")
        file_path = save_path
        # 解压缩文件
        zip_path = file_path + '/MaaResource-main.zip'
        file = zipfile.ZipFile(zip_path)
        file.extractall(file_path)
        file.close()
        # 移动文件
        for root, dirs, files in os.walk(file_path + '/MaaResource-main'):
            for file in files:
                update_file = os.path.join(root, file)
                save_file = update_file.replace('/MaaResource-main', '')
                if os.path.exists(save_file):
                    os.remove(save_file)
                shutil.move(update_file, save_file)
        # 删除文件
        shutil.rmtree(file_path + '/MaaResource-main')
        os.remove(zip_path)
        QMessageBox.information(self.ui, '提示', 'MAA更新版本成功')
