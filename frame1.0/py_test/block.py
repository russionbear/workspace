#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :block.py
# @Time      :2022/1/2 16:33
# @Author    :russionbear

import pygame
from standard.render.ui.menu import Menu
from standard.render.block import MapShowRender
from standard.core import Core

from standard.resource.manager import resManager

resManager.load_source(r'E:\workspace\workspace\test\source')
resManager.load_modes(r'E:\workspace\workspace\test\modes')


class CtrlWin:
    def __init__(self, win_size, map_path, block_size=(50, 50)):
        self.suf = pygame.display.set_mode(win_size)
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}
        self.menu = Menu(self.suf)
        self.center = MapShowRender(self.suf, block_size)
        self.center.load_map(map_path)

        self.__moveDirection = None
        self.__moveSpeed = 1
        size = self.center.get_size()
        self.__canMove = win_size[0] < size[0], win_size[1] < size[1]
        self.keyCtrlDown = False

    def update(self):
        if self.menu:
            self.menu.update()
        self.center.update()
        if self.__moveDirection is not None:
            pos = self.center.get_pos()
            size = self.center.get_size()
            size1 = self.suf.get_size()
            pos = pos[0] + self.__moveDirection[0] * self.__moveSpeed if self.__canMove[0] else 0, \
                pos[1] + self.__moveDirection[1] * self.__moveSpeed if self.__canMove[1] else 0
            x, y = pos
            if self.__canMove[0]:
                if pos[0] > 0:
                    x = 0
                elif pos[0] + size[0] < size1[0]:
                    x = size1[0] - size[0]
            if self.__canMove[1]:
                if pos[1] > 0:
                    y = 0
                elif pos[1] + size[1] < size1[1]:
                    y = size1[1] - size[1]
            if pos[0] == x and pos[1] == y:
                self.__moveDirection = None
            self.center.move(x, y)

    def event(self, e1):
        if e1.type == pygame.MOUSEBUTTONDOWN:
            if e1.button == 1:
                pass
            elif e1.button == 3:
                pass
        elif e1.type == pygame.MOUSEMOTION:
            x = y = 0
            _border = 25
            size1 = self.suf.get_size()
            if e1.pos[0] < _border:
                x = -1
            elif e1.pos[0] + _border > size1[0]:
                x = 1
            if e1.pos[1] < _border:
                y = -1
            elif e1.pos[1] + _border > size1[1]:
                y = 1
            if x != 0 or y != 0:
                self.__moveDirection = x, y
            else:
                self.__moveDirection = None

        elif e1.type == pygame.MOUSEBUTTONUP:
            if e1.button == 1:
                pass
            elif e1.button == 3:
                pass

        elif e1.type == pygame.KEYDOWN:
            if e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = True
        elif e1.type == pygame.KEYUP:
            if e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = False


Core.add(CtrlWin((600, 400), r'E:\workspace\workspace\test\maps\test.json'))
Core.run()
