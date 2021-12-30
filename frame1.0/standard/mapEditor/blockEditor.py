#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :blockEditor.py
# @Time      :2021/12/20 9:35
# @Author    :russionbear

import pygame
import sys, json, re

from typing import List, Dict

from ..core import Pen, Core
from ..resource import resManager, Spirit, UnitMaker, UnitLoader
# from ..geography import Spirit
import pickle, os

from PyQt5.Qt import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox \
    , QLabel, QFileDialog, QSize, \
    QListWidget, QListWidgetItem, QIcon, Qt
from PyQt5 import QtGui

Qapp = QApplication(sys.argv)


class BlockEditWin(QWidget):
    def __init__(self, win_size, path, is_new=True, *args):
        super(BlockEditWin, self).__init__()
        self.setFixedSize(win_size[0], win_size[1])
        self.res = resManager
        # self.res.load_source(source_path, True)
        self.resKeys = {}
        # for i in self.res.d:
        #     for k, v in zip(i.get_index_key(), i.get_index()):
        #         if k not in self.resKeys:
        #             self.resKeys[k] = set()
        #         self.resKeys[k].add(v)
        # for i in self.res.m:
        #     s0 = i.edit_path
        #     for j1, j in enumerate(s0.split('-')):
        #         if str(j1) not in self.resKeys:
        #             self.resKeys[str(j1)] = set()
        #         self.resKeys[str(j1)].add(j)

        # self.keys = []
        self.nowData = [i.edit_path for i in self.res.m]
        self.listView = None
        self.chosenData = None

        self.editView = BlockEditor(win_size, (50, 50), path)
        self.initUI()

        if is_new:
            self.editView.init_map(*args)
        else:
            self.editView.load()
        Core.add(self.editView)

    def initUI(self):
        layout = QVBoxLayout()

        # layout1 = QHBoxLayout()
        # for k, v in self.resKeys.items():
        #     tmp = QComboBox(self)
        #     tmp_l = list(v)
        #     tmp_l.append('')
        #     tmp.addItems(tmp_l)
        #     tmp.data = k
        #     tmp.setCurrentText('')
        #     tmp.currentTextChanged.connect(self.changed)
        #     self.keys.append(tmp)
        #     layout1.addWidget(QLabel(k, self))
        #     layout1.addWidget(tmp)
        #     layout1.addStretch(1)
        #
        # layout.addLayout(layout1)

        self.listView = QListWidget(self)
        self.listView.currentRowChanged.connect(self.choose)
        layout.addWidget(self.listView)
        self.listView.addItems(self.nowData)

        self.setLayout(layout)

    # def changed(self, n):
    #     keys = []
    #     for i in self.keys:
    #         keys.append(i.currentText())
    #         # keys[i.data] = i.currentText()
    #     keys.remove('')
    #
    #     s0 = '(-.*){1:}'.join(keys) + '-?.*'
    #
    #     rlt = []
    #     for i in self.res.m:
    #         if re.match(s0, i.edit_path) is not None:
    #             rlt .append()
    #         s0 = i.edit_path.split('-')
    #         for k, v in keys.items():
    #             if hasattr(i, k):
    #                 if getattr(i, k) != v:
    #                     break
    #         else:
    #             rlt.append(i)
    #     self.listView.clear()
    #     for i in rlt:
    #         # if i['images']:
    #         path = self.res.editPath[i]
    #         # tmp_k = {}
    #         # for j in self.keys:
    #         #     if hasattr(i, j.data):
    #         #     # if j.data in i:
    #         #         tmp_k[j.data] = i[j.data]
    #         self.listView.addItem(
    #             QListWidgetItem(QIcon(path),
    #                             os.path.split(os.path.split(path)[0])[1]))
    #     self.nowData = rlt

    def choose(self, t0):
        self.chosenData = self.nowData[t0]
        self.editView.set_chose(self.chosenData.split('-'))
        # print(resManager.editPath[self.chosenData])

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape:
            pass
            self.hide()
            # print(Core.listener)
            Core.run()
            self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pygame.quit()
        super(BlockEditWin, self).closeEvent(a0)


class MapSurf:
    def __init__(self, pen: pygame.surface.Surface, block_size):
        self.blockSize = block_size

        self.mapRl = 0, 0
        self.res = resManager

        self.pen = pen
        self.anchor = 0, 0
        self.suf = pygame.surface.Surface((1, 1))

        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.click = pygame.time.Clock()

        self.backGround = None
        self.border = 0, 0
        self.basicLayer: List[List[Spirit]] = []
        self.spirits: Dict[...:tuple:Spirit] = {}

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

        self.chose = None

        self.circleStart: tuple | ... = None
        self.circleRect: pygame.rect.Rect | ... = None
        self.circleLog = None

        # UnitMaker.make(['unit', 'red', 'bigman']).copy()

    def init_map(self, size, bg, border):
        self.basicLayer = [[None for i in range(size[0])] for j in range(size[1])]
        self.mapRl = size
        self.border = border
        self.suf = pygame.surface.Surface((size[0]*self.blockSize[0],
                                           size[1]*self.blockSize[1]))
        if bg:
            self.backGround = UnitMaker.make(bg)

    def load_map(self, path):
        with open(path, 'r') as f:
            tmp_d = json.load(f)
        if tmp_d['background'] is not None:
            self.backGround = resManager.get(args=tmp_d['background'])
        self.border = tuple(tmp_d['border'])
        self.basicLayer = []
        for i1, i in enumerate(tmp_d['basic_layer']):
            tmp_l = []
            for j1, j in enumerate(i):
                if j:
                    tmp_l.append(UnitLoader.load(j, self.suf))
                else:
                    tmp_l.append(None)
            self.basicLayer.append(tmp_l)

        self.mapRl = len(self.basicLayer[0]), len(self.basicLayer)

        for k, v in tmp_d['spirits'].items():
            tmp_l = {}
            for k1, v1 in v.items():
                tmp_l[k1] = UnitLoader.load(v, self.suf)
            self.spirits[int(k)] = tmp_l

        # self.scale(-1)

    def to_sequence(self):
        tmp_d = {'background': None, 'border': self.border}
        if self.backGround is not None:
            tmp_d['background'] = self.backGround.to_sequence()['track']

        tmp_d['basic_layer'] = []
        for i in self.basicLayer:
            tmp_l = []
            for j in i:
                if j:
                    tmp_l.append(j.to_sequence())
                else:
                    tmp_l.append(None)
            tmp_d['basic_layer'].append(tmp_l)

        tmp_d['spirits'] = {}
        for k, v in self.spirits.items():
            tmp_l = {}
            for k1, v1 in v.items():
                tmp_l[k1] = v1.to_sequence()
            tmp_d['spirits'][str(k)] = tmp_l
        return tmp_d

    def update(self):
        t0 = self.click.get_time()
        if self.backGround:
            self.backGround.update(t0)
        else:
            self.suf.fill((255, 255, 255))
        self.pen.blit(self.suf, self.anchor)

        # if self.backGround:
        #     size = self.scaleList[self.nowScalePoint]
        #     self.suf.blit(self.backGround, (size[0] * self.border[0], size[1] * self.border[1]))
        # else:

        for r in self.basicLayer:
            for l in r:
                if l:
                    l.update(t0)

        for k, v in self.spirits.items():
            for k1 in list(v.values()):
                k1.update(t0)

        if self.circleRect is not None:
            pygame.draw.rect(self.suf, (0, 255, 100), self.circleRect, 5)

        # for k, v in self.spirits.items():
        #     for k1, v1 in v.items():
        #         x, y = self.anchor[0] + k1[0] * self.blockSize[0], \
        #                self.anchor[1] + k1[1] * self.blockSize[1]
        #         self.suf.blit(v1, (x, y))

    def move(self, y=0, x=0, pos=None):
        if pos:
            y, x = pos
        self.anchor = self.anchor[0] + y, self.anchor[1] + x
        if self.backGround:
            size = self.scaleList[self.nowScalePoint]
            pos = self.anchor[0] - size[0] * self.border[0], \
                self.anchor[1] - size[1] * self.border[1]
            self.backGround.move(pos=pos)

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
        size_1 = size[0] * self.mapRl[0], \
            size[1] * self.mapRl[1]

        self.anchor = self.anchor[0] + (self.suf.get_width() - size_1[0]) / 2, \
            self.anchor[1] + (self.suf.get_height() - size_1[1]) / 2

        self.suf = pygame.surface.Surface(size_1)

        if self.backGround:
            pos = self.anchor[0] - size[0] * self.border[0], \
                self.anchor[1] - size[1] * self.border[1]
            size_2 = size_1[0] + size[0] * self.border[0] * 2, \
                size_1[1] + size[1] * self.border[1] * 2
            self.backGround.move(pos=pos)
            self.backGround.scale(size=size_2)

        for i1, i in enumerate(self.basicLayer):
            for j1, j in enumerate(i):
                if not j:
                    continue
                j.scale(self.suf, size)
                j.move(size[0]*j1, size[1]*i1)
                print('12', end='')

        for k, v in self.spirits.items():
            for k1, v1 in v.items():
                v1.scale(self.suf, size)
                v1.move(size[0]*k1[0], size[1]*k1[1])

        # bw, bh = size[0] // self.mapRl[0], size[1] // self.mapRl[1]
        # for i1, i in enumerate(self.map):
        #     for j1, j in enumerate(i):
        #         j.scale((bw, bh))
        #         j.move(j1*bw, i1*bh)

    def event(self, e1):
        def hand_rect():
            # e1.pos = min(e1.pos[0], self.suf.get_width()), \
            #          min(e1.pos[1], self.suf.get_height())
            return min(self.circleStart[0], e1.pos[0]) - self.anchor[0], \
                min(self.circleStart[1], e1.pos[1]) - self.anchor[1], \
                abs(self.circleStart[0] - e1.pos[0]), \
                abs(self.circleStart[1] - e1.pos[1])

        if e1.type == pygame.MOUSEBUTTONDOWN:
            self.circleStart = e1.pos
            pygame.event.set_grab(True)
            print('down', self.circleStart)
        elif e1.type == pygame.MOUSEMOTION:
            if self.circleStart is not None:
                self.circleRect = hand_rect()

        elif e1.type == pygame.MOUSEBUTTONUP:
            if self.circleStart:
                x, y, w, h = hand_rect()
                self.circleRect = x, y, w, h
                block_size = self.scaleList[self.nowScalePoint]
                x1, y1 = x // block_size[0], y // block_size[1]
                x2, y2 = (x+w) // block_size[0] + 1, (y+h) // block_size[1] + 1

                print(x1, x2, y1, y2, x, y)
                self.cover(x1, x2, y1, y2)

                self.circleStart = None
                self.circleRect = None

    def handle(self, e1):
        pass

    def check(self):
        pass

    def set_chose(self, key):
        self.chose = UnitMaker.make(key)

    def clear_log(self):
        if self.circleLog is not None:
            for i1 in range(self.circleLog[0], self.circleLog[1]):
                for j1 in range(self.circleLog[2], self.circleLog[3]):
                    for k, v in self.spirits.items():
                        if (j1, i1) in v:
                            del v[(j1, i1)]
                    self.basicLayer[j1][i1] = None

    def cover(self, x1, x2, y1, y2):
        if self.chose:
            x1, y1 = max(int(x1), 0), max(int(y1), 0)
            x2, y2 = min(int(x2), self.mapRl[0]), \
                min(int(y2), self.mapRl[1])
            layer = self.chose.get_layer()
            size = self.scaleList[self.nowScalePoint]
            if layer == 1:
                for i1 in range(y1, y2):
                    for j1 in range(x1, x2):
                        obj = self.chose.copy()
                        self.basicLayer[i1][j1] = obj
                        obj.set_pen(self.suf)
                        obj.scale(size=size)
                        obj.move(j1 * size[0], i1 * size[1])
            else:
                for i1 in range(y1, y2):
                    for j1 in range(x1, x2):
                        if layer not in self.spirits:
                            self.spirits[layer] = {}
                            tmp_d = {}
                            tmp_k = set(list(self.spirits.keys()))
                            for i in tmp_d:
                                tmp_d[i] = self.spirits[i]
                            self.spirits = tmp_k

                        obj = self.chose.copy()
                        self.spirits[layer][(j1, i1)] = obj
                        obj.set_pen(self.suf)
                        obj.scale(size=size)
                        obj.move(j1 * size[0], i1 * size[1])

            self.circleLog = x1, x2, y1, y2


class BlockEditor:
    def __init__(self, win_size, block_size, save_path):
        self.suf = pygame.display.set_mode(win_size)
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}
        self.bgColor = pygame.color.Color(0, 0, 0)

        self.mapSuf = MapSurf(self.suf, block_size)

        self.chose = None

        self.keyCtrlDown = False

        self.savePath = save_path

    def load(self):
        self.mapSuf.load_map(self.savePath)

    def init_map(self, size, bg=None, border=(0, 0)):
        self.mapSuf.init_map(size, bg, border)

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
            elif e1.button == 1:
                self.mapSuf.event(e1)

        elif e1.type == pygame.MOUSEBUTTONUP:
            pygame.event.set_grab(False)
            if e1.button == 1:
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
            elif e1.key == pygame.K_DELETE:
                print('fdffdfd')
                self.mapSuf.clear_log()

    def save(self):
        with open(self.savePath, 'w', encoding='utf-8') as f:
            json.dump(self.mapSuf.to_sequence(), f, indent=4)
            # f.write(pickle.dumps(self))

    def set_chose(self, key):
        self.mapSuf.set_chose(key)

    @staticmethod
    def load_obj(file_path):
        with open(file_path, 'r') as f:
            return pickle.load(f)
