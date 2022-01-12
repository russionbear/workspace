#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :menuWin.py
# @Time      :2022/1/10 11:08
# @Author    :russionbear


import pygame
from ..ui.listView import ListView
from ..ui.menu import Menu
from ..layout import Layout


class MenuWinArea:
    def __init__(self, rect):
        self.data = {}
        self.layout = 0
        self.align = None
        self.rect: pygame.rect.Rect = rect

    def update(self):
        for k, v in self.data.items():
            v.update()

    def move(self, x=0, y=0, pos=None):
        if pos is not None:
            x, y = pos
        self.rect.move(x, y)
        func = Layout.get_layout(self.layout)
        if func:
            func(list(self.data.values()), self.rect, self.align)

    def get_size(self):
        return self.rect.size

    def set_layout(self, layout, align=0):
        self.layout = layout
        self.align = align
        func = Layout.get_layout(layout)
        if func:
            func(list(self.data.values()), self.rect, align)

    def add_item(self, tag, size, items):
        pass

    def contains(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            for k, v in self.data.items():
                track = v.contains(pos)
                if track:
                    return k, track


class MenuWinPage:
    def __init__(self):
        self.areas = {}



class MenuWin:
    def __init__(self, size, bgt0=None):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN}
        self.suf = pygame.display.set_mode(size)
        self.pages = {}

        self.listener = None
        self.nowTitle = None

    def set_layout(self, title, layout, area=None):
        pass

    def add_menu(self, title, area, size, items, bgt0=None):
        if title not in self.pages:
            self.pages = {}
        if area not in self.pages:
            pass

        obj = Menu(self.suf, size, bgt0)
        obj.add_items(items)
        Layout.vertical_box(obj.children(), obj.get_rect())
        self.pages[title].add(obj)

        # Layout.horizontal_box(list(self.pages.values()), self.suf.get_rect())
        Layout.horizontal_box([obj], self.suf.get_rect())
        self.swap(title)

    def add_list_view(self, title, data):
        obj = ListView(self.suf, self.suf.get_size(), data)
        Layout.vertical_box([obj], self.suf.get_rect())
        self.pages[title] = obj

    def update(self):
        self.suf.fill((0, 0, 0))
        if self.listener:
            self.listener.update()

    def swap(self, title):
        self.listener = self.pages[title]
        self.nowTitle = title

    def event(self, e0):
        if e0.button != 1 or not self.listener:
            return
        return self.listener.contains(e0.pos)

