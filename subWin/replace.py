import os

from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog


def GitReplace(obj, path, start, end, suffix=''):
    # 获取文件夹下除.git的所有文件目录
    file_paths = []
    for folder_name, sub_folders, file_names in os.walk(path):
        sub_folders[:] = [d for d in sub_folders if not d.startswith('.')]
        file_names[:] = [f for f in file_names if not f.startswith('.')]
        for filename in file_names:
            file_paths.append(os.path.join(folder_name, filename))
    if suffix == '':
        suffix = '.md'
    for f in file_paths:
        if f.endswith(suffix):
            with open(f, 'r', encoding='utf-8') as file:
                content = file.readlines()
                res_list = []
            for line in content:
                res = line.replace(start, end)
                res_list.append(res + '\n')
            with open(f, 'w', encoding='utf-8') as file:
                file.writelines(res_list)
            obj.insertPlainText(f + '\n')


class replaceWin:

    def __init__(self):
        self.ui = QUiLoader().load('ui/replace.ui')
        self.ui.btnStart.clicked.connect(self.Convert)
        self.ui.selectFilePath.clicked.connect(self.selectFilePath)

    def Convert(self):
        path = self.ui.pathText.text()
        suffix = self.ui.suffixText.text()
        start = self.ui.beforeText.text()
        end = self.ui.replaceText.text()
        GitReplace(self.ui.textBrowser, path, start, end, suffix)

    def selectFilePath(self):
        # 打开文件浏览界面
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 获取文件路径
        file_path = QFileDialog.getExistingDirectory(self.ui, "选取文件夹", "./")
        self.ui.pathText.setText(file_path)
