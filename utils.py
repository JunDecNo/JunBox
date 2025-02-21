# 获得根目录
import os
import threading

def getRootPath():
    root_path = os.getcwd().replace('\\', '/').split('/')
    root_path = root_path[0: len(root_path)]
    root_path = '/'.join(root_path)
    return root_path


