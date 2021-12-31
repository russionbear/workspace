#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :blockEditor.py
# @Time      :2021/12/20 9:35
# @Author    :russionbear

import pygame
import sys, json, re

from typing import List, Dict

from ..core import Pen, Core
from ..resource import resManager
from ..mapCtrl import MapEditRender
import pickle, os

from PyQt5.Qt import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox \
    , QLabel, QFileDialog, QSize, \
    QListWidget, QListWidgetItem, QIcon, Qt
from PyQt5 import QtGui

Qapp = QApplication(sys.argv)

# resManager = ResMngMaker.init('edit')


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


class BlockEditor:
    def __init__(self, win_size, block_size, save_path):
        self.suf = pygame.display.set_mode(win_size)
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}
        self.bgColor = pygame.color.Color(0, 0, 0)

        self.mapSuf = MapEditRender(self.suf, block_size)

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
