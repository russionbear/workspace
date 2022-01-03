#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ui.py
# @Time      :2022/1/2 16:40
# @Author    :russionbear
import pygame
from ..standard.core import Core
from ..standard.render.ui.menu import Menu


class TestWin:
    def __init__(self, size, s0=None):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN}
        self.suf = pygame.display.set_mode(size)
        self.menu = Menu(self.suf, s0, 12, 12)
        self.menu.add_items(['images', 'images', 'images'])

    def update(self):
        self.suf.fill((0, 0, 0))
        self.menu.update()

    def event(self, e0):
        if e0.type == pygame.MOUSEBUTTONDOWN:
            if e0.button == 1:
                print(self.menu.contains(e0.pos))


Core.add(TestWin((600, 400)))
Core.run()
