#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :blockEditor.py
# @Time      :2021/12/20 9:35
# @Author    :russionbear

import pygame
import sys, json

from typing import List

from ..core import Pen, Core
from ..resource import Resource, ResManager
from ..geography import Spirit
import pickle, os

from PyQt5.Qt import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox \
    , QLabel, QFileDialog, QSize, \
    QListWidget, QListWidgetItem, QIcon, Qt
from PyQt5 import QtGui

Qapp = QApplication(sys.argv)


class BlockEditWin(QWidget):
    def __init__(self, win_size, block_size, map_size, source_path):
        super(BlockEditWin, self).__init__()
        self.setFixedSize(win_size[0], win_size[1])
        self.res = ResManager(block_size, source_path)
        self.res.load_source(source_path, True)
        self.resKeys = {}
        for i in self.res.d:
            for k, v in i.items():
                # if isinstance(v, int) or isinstance(v, float) or isinstance(v, str):

                if isinstance(v, str) and k != 'filepath':
                    pass
                else:
                    continue
                if k not in self.resKeys:
                    self.resKeys[k] = set()
                self.resKeys[k].add(v)

        self.keys = []
        self.nowData = []
        self.listView = None
        self.chosenData = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        for k, v in self.resKeys.items():
            tmp = QComboBox(self)
            tmp_l = list(v)
            tmp_l.append('')
            tmp.addItems(tmp_l)
            tmp.data = k
            tmp.setCurrentText('')
            tmp.currentTextChanged.connect(self.changed)
            self.keys.append(tmp)
            layout1.addWidget(QLabel(k, self))
            layout1.addWidget(tmp)
            layout1.addStretch(1)

        layout.addLayout(layout1)

        self.listView = QListWidget(self)
        self.listView.currentRowChanged.connect(self.choose)
        layout.addWidget(self.listView)

        self.setLayout(layout)

    def changed(self, n):
        keys = {}
        for i in self.keys:
            if i.currentText() == '':
                continue
            keys[i.data] = i.currentText()

        rlt = []
        for i in self.res.d:
            for k, v in keys.items():
                if k in i:
                    if i[k] != v:
                        break
            else:
                rlt.append(i)
        self.listView.clear()
        for i in rlt:
            # if i['images']:
            path = i['filepath']
            tmp_k = {}
            for j in self.keys:
                if j.data in i:
                    tmp_k[j.data] = i[j.data]
            self.listView.addItem(QListWidgetItem(QIcon(path), json.dumps(tmp_k)))
        self.nowData = rlt

    def choose(self, t0):
        self.chosenData = self.nowData[t0]

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape:
            pass
            self.hide()
            Core.run()
            self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pygame.quit()
        super(BlockEditWin, self).closeEvent(a0)


class MapSurf:
    def __init__(self, pen: pygame.surface.Surface, block_size, map_size, source: ResManager):
        self.blockSize = block_size
        self.priSize = map_size
        self.mapRl = map_size[0] // block_size[0], map_size[1] // block_size[1]
        self.res = source

        self.pen = pen
        self.anchor = 0, 0
        self.suf = pygame.surface.Surface(map_size)

        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.map: List[List[Spirit]] = []

        self.bgColor = pygame.color.Color(0, 0, 0)

        size = block_size
        self.scaleList = [size]
        self.nowScalePoint = 0
        while 1:
            if size[0] < block_size[0] // 4 and \
                    size[1] < block_size[1] // 4:
                break
            size = int(size[0] / 1.2), int(size[1] / 1.2)
            self.scaleList.insert(0, size)
            self.nowScalePoint += 1
        size = block_size
        while 1:
            if size[0] > block_size[0] * 4 and \
                    size[1] > block_size[1] * 4:
                break
            size = int(size[0] * 1.2), int(size[1] * 1.2)
            self.scaleList.append(size)

        self.keyCtrlDown = False

    def init_map(self):
        pass

    def update(self):
        self.pen.blit(self.suf, self.anchor)
        self.suf.fill(self.bgColor)
        t0 = pygame.time.Clock().get_time()
        for r in self.map:
            for l in r:
                l.update(t0)

    def move(self, y=0, x=0, pos=None):
        if pos:
            y, x = pos
        self.anchor = self.anchor[0] + y, self.anchor[1] + x

    def scale(self, n):
        if n > 0:
            if self.nowScalePoint + 1 == len(self.scaleList):
                return
            self.nowScalePoint += 1
        else:
            if self.nowScalePoint == 0:
                return
            self.nowScalePoint -= 1
        size = self.scaleList[self.nowScalePoint]

        self.anchor = self.anchor[0] + (self.suf.get_width() - size[0]) / 2, \
                      self.anchor[1] + (self.suf.get_height() - size[1]) / 2

        self.suf = pygame.surface.Surface(size)

        bw, bh = size[0] // self.mapRl[0], size[1] // self.mapRl[1]
        for i1, i in enumerate(self.map):
            for j1, j in enumerate(i):
                j.scale((bw, bh))
                j.move(j1*bw, i1*bh)

    def event(self, e1):
        pass

    def handle(self, e1):
        pass


class BlockEditor:
    def __init__(self, win_size, map_suf: MapSurf, save_path):
        self.suf = pygame.display.set_mode(win_size)
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}
        self.bgColor = pygame.color.Color(0, 0, 0)

        self.mapSuf = map_suf
        self.mapSuf.pen = self.suf

        self.keyCtrlDown = False

        self.savePath = save_path

    def update(self):
        self.suf.fill(self.bgColor)
        self.mapSuf.update()

    def event(self, e1):
        if e1.type == pygame.MOUSEMOTION:
            if e1.buttons[2]:
                self.mapSuf.move(pos=e1.rel)
                pygame.event.set_grab(True)
            elif e1.buttons[0]:
                self.mapSuf.event(e1)

        elif e1.type == pygame.MOUSEBUTTONDOWN:
            if e1.button == 5:
                self.mapSuf.scale(-1)
            elif e1.button == 4:
                self.mapSuf.scale(1)
            elif e1.button == 0:
                self.mapSuf.event(e1)

        elif e1.type == pygame.MOUSEBUTTONUP:
            pygame.event.set_grab(False)
            self.mapSuf.event(e1)

        elif e1.type == pygame.KEYDOWN:
            if e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = True
            elif e1.key == pygame.K_s:
                if not self.keyCtrlDown:
                    return
                self.save()
            elif e1.key == pygame.K_q:
                if not self.keyCtrlDown:
                    return
                Core.overed = True
        elif e1.type == pygame.KEYUP:
            if e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = False

    def save(self):
        with open(self.savePath, 'wb') as f:
            f.write(pickle.dumps(self))

    @staticmethod
    def load_obj(file_path):
        with open(file_path, 'r') as f:
            return pickle.load(f)
