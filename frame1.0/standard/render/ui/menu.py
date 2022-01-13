#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :menu.py
# @Time      :2021/12/31 16:39
# @Author    :russionbear
from typing import List, Dict
from .. import resManager, Pen
from ..layout import Layout
import pygame

pygame.init()


def make_text_image(text, font, size):
    pass


class MenuItem:
    def __init__(self, pen, text=None, bgt0=None, width=None):
        self.__pen = pen
        self.__anchor = 0, 0

        self.__nowImage = None

        if bgt0 is not None:
            self.__nowImage = resManager.get_menu_image(bgt0)
            size = self.__nowImage.get_size()
            if width is None:
                width = Pen.get_font_size()
            size = width, width * size[1] // size[0]
            self.__nowImage = pygame.transform(self.__nowImage, size)

            self.__key = bgt0[-1]
        else:
            self.__textSuf = Pen.render(text)
            self.__key = text

    def update(self):
        if self.__nowImage:
            self.__pen.blit(self.__nowImage, self.__anchor)
            """debug"""
            pygame.draw.rect(self.__pen, (0, 255, 100),
                             self.__nowImage.get_rect().move(self.__anchor[0], self.__anchor[1]), 4)

        else:
            self.__pen.blit(self.__textSuf, self.__anchor)
            """debug"""
            # pygame.draw.rect(self.__pen, (0, 255, 100),
            #                  self.__textSuf.get_rect().move(self.__anchor[0], self.__anchor[1]), 4)

    def contains(self, pos):
        if self.__nowImage:
            return self.__nowImage.get_rect().move(self.__anchor[0], self.__anchor[1]).collidepoint(pos[0], pos[1])
        else:
            return self.__textSuf.get_rect().move(self.__anchor[0], self.__anchor[1]).collidepoint(pos[0], pos[1])

    def set_pen(self, pen):
        self.__pen = pen

    def get_size(self):
        if self.__nowImage:
            return self.__nowImage.get_size()
        else:
            return self.__textSuf.get_size()

    # def scale(self, size):
    #     self.__nowImage = pygame.transform.scale(self.__nowImage, size)

    def move(self, x=0, y=0, pos=None):
        if pos is not None:
            x, y = pos
        self.__anchor = x, y

    def get_pos(self):
        return self.__anchor

    def get_key(self):
        return self.__key


class Menu:
    def __init__(self, pen, size, bgt0=None):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN}

        self.__pen = pen
        self.__anchor = 0, 0
        self.__suf = pygame.surface.Surface(size)

        self.__children: List[MenuItem] = []

        self.__bg = None
        if bgt0 is not None:
            self.__bg = resManager.get_menu_image(bgt0)

        # self.__showed = True

        self.__callBack = None
        self.__id = None

    # def scale(self, rate):
    #     size = self.__suf.get_size()
    #     size = int(size[0] * rate), int(size[1] * rate)
    #     self.__suf = pygame.surface.Surface(size)
    #     self.__bg = pygame.transform.scale(self.__bg, size)
    #     for i in self.__children:
    #         size = i.get_size()
    #         size = int(size[0] * rate), int(size[1] * rate)
    #         i.scale(size)
    #         i.set_pen(self.__suf)
    #         size = i.get_pos()
    #         size = int(size[0] * rate), int(size[1] * rate)
    #         i.move(size)

    def set_call_back(self, func, id_=None):
        self.__callBack = func
        self.__id = id_

    def add_items(self, items):
        for i in items:
            if isinstance(i, str):
                obj = MenuItem(self.__suf, i)
            else:
                obj = MenuItem(self.__suf, bgt0=i[0], width=i[1])
            self.__children.append(obj)

    def move(self, x=0, y=0, pos=None):
        if pos is not None:
            x, y = pos
        self.__anchor = x, y
        print(x, y, 'move')

    def update(self):
        # if not self.__showed:
        #     return
        self.__pen.blit(self.__suf, self.__anchor)
        if self.__bg:
            self.__suf.blit(self.__bg, (0, 0))
        for i in self.__children:
            i.update()
        """debug"""
        pygame.draw.rect(self.__pen, (0, 255, 100),
                         self.__suf.get_rect().
                         move(self.__anchor[0], self.__anchor[1]),
                         4)

    def event(self, e0):
        if not self.contains(e0.pos) or e0.button != 1:
            self.__showed = False
            return

        # if not self.__showed:
        #     self.__showed = True

        for i in self.__children:
            if i.contains(e0.pos):
                if self.__callBack:
                    self.__callBack(self.__id, i.get_key())
                self.__showed = False
                break
                # return i.get_key()

    def contains(self, pos):
        return self.__suf.get_rect().\
            move(self.__anchor).\
            collidepoint(pos)
        # print(pos)
        # for i in self.__children:
        #     if i.contains(pos):
        #         return i.get_key()

    def clear(self):
        self.__children.clear()

    def show(self):
        self.__showed = True

    def hide(self):
        self.__showed = False

    def get_size(self):
        return self.__suf.get_size()

    def get_pos(self):
        return self.__anchor

    def get_rect(self):
        return self.__suf.get_rect()
        # return self.__suf.get_rect().move(self.__anchor)

    def set_bg(self, name):
        self.__bg = pygame.transform.scale(resManager.get_menu_image(name), self.__suf.get_size())

    def children(self):
        return self.__children


class MenuWin:
    def __init__(self, size, bgt0=None):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN}
        self.suf = pygame.display.set_mode(size)
        self.menus = {}

        self.listener = None
        self.nowTitle = None

    def add_menu(self, title, size, items, bgt0=None):
        obj = Menu(self.suf, size, bgt0)
        obj.add_items(items)
        Layout.vertical_box(obj.children(), obj.get_rect())
        self.menus[title] = obj

        # Layout.horizontal_box(list(self.menus.values()), self.suf.get_rect())
        Layout.horizontal_box([obj], self.suf.get_rect())
        self.swap(title)

    def update(self):
        self.suf.fill((0, 0, 0))
        if self.listener:
            self.listener.update()

    def swap(self, title):
        self.listener = self.menus[title]
        self.nowTitle = title

    def event(self, e0):
        if e0.button != 1 or not self.listener:
            return
        return self.listener.contains(e0.pos)




