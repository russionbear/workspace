#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :window.py
# @Time      :2022/1/12 15:08
# @Author    :russionbear

import pygame


class GWindow:
    def __init__(self, size):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                           pygame.MOUSEBUTTONUP,
                           pygame.MOUSEMOTION,
                           pygame.KEYUP,
                           pygame.KEYDOWN}
        self.suf = pygame.display.set_mode(size)

        # self.input = None
        # self.scroll = None
        # self.drag = None
        self.children = []
        # self

    def add(self, obj):
        self.children.append(obj)

    def event(self, e0):
        for i in self.children:
            if e0.type in i.legalEvents:
                i.event(e0)

    def update(self):
        self.suf.fill((0, 0, 0))
        for i in self.children:
            i.update()

