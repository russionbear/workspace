# coding:utf-8
from PyQt5.Qt import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox\
    , QSpinBox, QPixmap, QPushButton, QLabel, QFileDialog
from PyQt5 import QtCore, QtGui
import sys, shutil, os
from .bgEditor import MainView
from ..core import Core


Qapp = QApplication(sys.argv)


class WinStrategyEditor(QWidget):
    def __init__(self, root):
        super(WinStrategyEditor, self).__init__()
        self.types = ['简单背景', '层级块', '层级粉刷']
        self.initUI()
        self.root = root

    def initUI(self):
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        layout1 = QHBoxLayout()

        layout1.addWidget(QLabel('地图类型'))
        tmp = QComboBox(self)
        tmp.addItems(self.types)
        tmp.currentTextChanged.connect(self.swap_menu)
        self.typeCom = tmp
        layout1.addWidget(tmp)
        layout1.addStretch(1)

        layout1.addWidget(QLabel('编辑器宽高：'))
        tmp = QSpinBox(self)
        tmp.setMaximum(1960)
        tmp.setMinimum(400)
        tmp.setValue(600)
        tmp.setSingleStep(100)
        layout1.addWidget(tmp)
        tmp = QSpinBox(self)
        tmp.setMaximum(1080)
        tmp.setSingleStep(100)
        tmp.setMinimum(400)
        layout1.addWidget(tmp)

        layout.addLayout(layout1)

        layout1 = QHBoxLayout()
        self.layer1 = []
        tmp = QLabel(self)
        self.layer1.append(tmp)
        self.image = tmp
        self.image.filepath = None
        layout1.addWidget(tmp)
        tmp = QPushButton('选择文件', self)
        tmp.clicked.connect(self.open_file)
        self.layer1.append(tmp)
        layout1.addWidget(tmp)

        layout.addLayout(layout1)

        tmp = QPushButton('开始编辑', self)
        tmp.clicked.connect(self.edit)
        layout.addWidget(tmp)

        self.setLayout(layout)

    def swap_menu(self, t0):
        if t0 == self.types[0]:
            pass
        pass

    def open_file(self):
        directory = QFileDialog.getOpenFileName(self, "选择图片", "./", "(*.jpg)")

        p = QPixmap(directory[0])
        if p.width() > p.height():
            p = p.scaledToHeight(self.height()//2)
        else:
            p = p.scaledToWidth(self.width()//2)
        self.image.setPixmap(p)
        self.image.filepath = directory[0]

    def edit(self):
        if self.typeCom.currentText() == self.types[0]:
            if not self.image.filepath:
                return
            if os.path.exists(self.root):
                shutil.rmtree(self.root)
            os.mkdir(self.root)
            shutil.copy(self.image.filepath, self.root+'/map.jpg')
            Core.add(MainView(self.root))
            Core.run()

