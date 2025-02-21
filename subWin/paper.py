import json
import os
import shutil
import subprocess
import zipfile
import requests
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog, QMessageBox
from utils import getRootPath


def get_paper_info(doi):
    url = f'https://api.crossref.org/works/{doi}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            paper_info = response.json()['message']
            title = paper_info.get('title', ['Unknown'])[0]
            journal = paper_info.get('container-title', ['Unknown'])[0]
            authors = [author['given'] + ' ' + author['family'] for author in paper_info.get('author', [])]
            published_date = paper_info.get('issued', {}).get('date-parts', [['Unknown']])[0]
            pdf_link = paper_info.get('link', ['Unknown'])[0]['URL']
            return {
                'title': title,
                'journal': journal,
                'authors': authors,
                'published_date': '-'.join(map(str, published_date)),
                'pdf': pdf_link
            }
        else:
            return {'error': 'Paper not found'}
    except Exception as e:
        return {'error': str(e)}


class paperWin:
    def __init__(self):
        self.ui = QUiLoader().load('ui/paper.ui')
        self.ui.btnAna.clicked.connect(self.Analyze)
        self.ui.btnFile.clicked.connect(self.selectFilePath)
        self.ui.btnUpload.clicked.connect(self.Upload)
        self.jsonData = json.load(open(getRootPath() + '/subWin/config.json', 'r', encoding='utf-8'))

    def Analyze(self):
        doi_str = self.ui.doiPath.text()
        paper_dict = get_paper_info(doi_str)
        try:
            self.ui.title.setText(paper_dict['title'])
            self.ui.venue.setText(paper_dict['journal'])
            self.ui.date.setText(paper_dict['published_date'])
            self.ui.author.setText(", ".join(paper_dict['authors']))
            if "pdf" in paper_dict['pdf']:
                self.ui.pdf.setText(paper_dict['pdf'])
        except:
            return

    def selectFilePath(self):
        # 打开文件浏览界面
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # 获取文件路径
        file_path = QFileDialog.getExistingDirectory(self.ui, "选取文件夹", "./")
        self.ui.jsonPath.setText(file_path)

    def Upload(self):
        up_dict = {
            'title': self.ui.title.text(),
            'venue': self.ui.venue.text(),
            'date': self.ui.date.text(),
            'authors': self.ui.author.text(),
            'doi': self.ui.doiPath.text(),
        }
        if "https://doi.org/" not in up_dict['doi']:
            up_dict['doi'] = 'https://doi.org/' + up_dict['doi']
        if self.ui.pdf.text().strip().endswith('.pdf'):
            up_dict['pdf'] = self.ui.pdf.text()
        if self.ui.repo.text().strip() != "":
            up_dict['repo'] = self.ui.repo.text()
        if self.ui.img.text().strip() != "":
            up_dict['img'] = self.ui.img.text()
        json_path = self.jsonData["paper_json"] if self.ui.jsonPath.text().strip() == "" else self.ui.text.text()

        with open(json_path, "r", encoding='utf-8') as f:
            paper_json = json.load(f)
        # 加入
        paper_json[0].append(up_dict)
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(paper_json, f)
        proc = subprocess.run(f'hexo clean && hexo g && hexo d', shell=True, cwd=self.jsonData['hexo_root'])
        if proc.returncode == 0:
            QMessageBox.information(self.ui, '提示', '执行成功')
