#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :menu.py
# @Time      :2021/12/31 16:39
# @Author    :russionbear
from typing import List, Dict
from .resource import resManager
import pygame

pygame.init()


def make_text_image(text, font, size):
    pass


class MenuItem:
    def __init__(self, pen, t0):
        self.__pen = pen
        self.__anchor = 0, 0
        self.__nowImage = resManager.get_menu_image(t0)
        self.__key = t0

    def update(self):
        self.__pen.blit(self.__nowImage, self.__anchor)
        # pygame.draw.rect(self.__pen, (0, 255, 100), self.__nowImage.get_rect().move(self.__anchor[0], self.__anchor[1]), 4)

    def contains(self, pos):
        return self.__nowImage.get_rect().move(self.__anchor[0], self.__anchor[1]).collidepoint(pos[0], pos[1])

    def set_pen(self, pen):
        self.__pen = pen

    def get_size(self):
        return self.__nowImage.get_size()

    def scale(self, size):
        self.__nowImage = pygame.transform.scale(self.__nowImage, size)

    def set_pos(self, pos):
        self.__anchor = pos

    def get_pos(self):
        return self.__anchor

    def get_key(self):
        return self.__key


class Menu:
    def __init__(self, pen, t0=None, space=0, border=0, width=30):
        self.__pen = pen
        self.__anchor = 0, 0
        self.__children: List[MenuItem] = []
        self.__suf = pygame.surface.Surface((1, 1))
        self.__bg = None if t0 is None else resManager.get_menu_image(t0)
        self.__width = width
        self.__border = border
        self.__space = space
        self.__showed = True

    def add_items(self, items):
        w, h = 0, -self.__space
        items = list(set(items))
        for i in items:
            obj = MenuItem(self.__suf, i)
            size = obj.get_size()
            n = self.__width / size[0]
            obj.scale((int(n*size[0]), int(n*size[1])))
            obj.set_pos((self.__border, h+self.__space+self.__border))
            # print(obj.get_pos())
            size = obj.get_size()
            w = max(w, size[0])
            h += size[1] + self.__space
            self.__children.append(obj)

        self.__suf = pygame.surface.Surface(
            (w+self.__border*2, h+self.__border*2))
        if self.__bg:
            self.__bg = pygame.transform.scale(self.__bg, self.__suf.get_size())
        for i in self.__children:
            i.set_pen(self.__suf)
        # self.scale(self.__rate)

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
    #         i.set_pos(size)

    def move(self, x=0, y=0, pos=None):
        if pos is not None:
            x, y = pos
        self.__anchor = x, y

    def update(self):
        if not self.__showed:
            return
        self.__pen.blit(self.__suf, self.__anchor)
        if self.__bg:
            self.__suf.blit(self.__bg, (0, 0))
        for i in self.__children:
            i.update()
        # pygame.draw.rect(self.__pen, (0, 255, 100), self.__suf.get_rect(), 4)

    def contains(self, pos):
        pos = pos[0] - self.__anchor[0], pos[1] - self.__anchor[1]
        if not self.__suf.get_rect().collidepoint(pos[0], pos[1]):
            return None
        print(pos)
        for i in self.__children:
            if i.contains(pos):
                return i.get_key()
        return False

    def clear(self):
        self.__children.clear()

    def show(self):
        self.__showed = True

    def hide(self):
        self.__showed = False

    def get_size(self):
        return self.__suf.get_size()

    def set_bg(self, name):
        self.__bg = pygame.transform.scale(resManager.get_menu_image(name), self.__suf.get_size())


class TestWin:
    def __init__(self, size, s0):
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

