import subprocess
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog, QMessageBox
import markdown2
import json
from datetime import datetime


def str2tag(s):
    s_list = s.split(' ')
    res = ''
    for i in range(len(s_list)):
        res += f' - {s_list[i]}\n'
    return res


class hexoWin:
    def __init__(self):
        self.ui = QUiLoader().load('ui/hexo.ui')
        self.ui.btnStart.clicked.connect(self.deploy)
        self.ui.btnFile.clicked.connect(self.selectFilePath)
        self.jsonData = json.load(open('config.json', 'r', encoding='utf-8'))

    def deploy(self):
        summary = self.ui.summary.text()
        tag = str2tag(self.ui.tag.text())
        category = self.ui.category.text()
        img = self.ui.img.text()
        title = self.ui.mdPath.text().split('/')[-1].split('.')[0]
        author = self.jsonData['author']
        hexo_post = self.jsonData['hexo_post']
        with open(f'{hexo_post}{title}.md', 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(f'title: {title}\n')
            f.write(f'date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'author: {author}\n')
            f.write(f'summary: {summary}\n')
            f.write(f'tags: \n{tag}\n')
            f.write(f'categories: {category}\n')
            f.write(f'mathjax: true\n')
            if img != '':
                f.write(f'img: {img}\n')
            f.write('---\n')
            f.write(open(self.ui.mdPath.text(), 'r', encoding='utf-8').read())
        proc = subprocess.run(f'hexo clean && hexo g && hexo d', shell=True, cwd=self.jsonData['hexo_root'])
        if proc.returncode == 0:
            QMessageBox.information(self.ui, '提示', '执行成功')

    def selectFilePath(self):
        # 打开文件浏览界面
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 获取文件路径
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "选取文件", '', 'Markdown Files (*.md);;All Files (*)')
        self.ui.mdPath.setText(file_path)
        html = markdown2.markdown_path(file_path)
        self.ui.textBrowser.setHtml(html)
