#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :geography.py
# @Time      :2021/12/19 10:07
# @Author    :russionbear
import pygame
from typing import List, Dict

from .resource import resManager, Source, Mode
# from .core import Core


class Shard:
    def __init__(self,
                 pen: pygame.surface.Surface,
                 source: Source):
        self.__pen = pen
        # 100
        self.__offsetRate = 0, 0
        self.__offsetSize = 0, 0
        self.__anchor = 0, 0
        self.__source = source

    def set_pen(self, pen):
        self.__pen = pen

    def swap_action(self, name, type_=None):
        if type_ is None:
            self.__source.swap(name)

    def update(self, t0):
        self.__pen.blit(self.__source.get(), self.__anchor)
        self.__source.update(t0)

    # def slots(self, type_, **kwargs):
    #     pass

    def move(self, x=0, y=0, pos=None):
        if pos:
            x, y = pos
        self.__anchor = x, y

    def set_offset_size(self, d0):
        self.__offsetSize = d0

    def scale(self, pen):
        size = pen.get_size()
        self.__source.scale_to((size[0] * self.__offsetSize[0],
                                size[1] * self.__offsetSize[1]
                                ))
        self.__anchor = size[0] * self.__offsetRate[0] / 100, \
                        size[1] * self.__offsetRate[1] / 100

        self.__pen = pen

    def get_size(self):
        return self.__source.get_size()


class Spirit:
    def __init__(self, size, obj: Mode, pen):
        self.__pen = pen
        self.__suf = pygame.surface.Surface(size)
        # 100
        self.__offsetRate = 0, 0
        self.__offsetSize = 0, 0
        self.__anchor = 0, 0

        self.__source = obj
        self.__body: Dict[str, ...] = {}
        for k, v in obj.get_body().items():
            self.__body[k] = Shard(self.__suf, v.copy())

        self.__action = {}
        # self.__collideRect = 0, 0, 0, 0
        self.__renderOrder: list = []

        self.swap(obj.get_first_action()[0], obj.get_first_action()[1])

    def swap(self, name, type_=None):
        action = self.__source.get_action(name, type_)
        if 'layer' in action:
            self.__renderOrder = action['layer']
            for i in self.__renderOrder:
                self.__body[i].move(pos=action['offsetRate'][i])
                self.__body[i].set_offset_size(action['offsetSize'][i])
        if 'to' in action:
            for k, v in action['and'].items():
                self.__body[k].swap(name, type_)
        self.__action[type_] = name

    def update(self, t0):
        self.__pen.blit(self.__suf, self.__anchor)
        for i in self.__renderOrder:
            self.__body[i].update(t0)

    def slots(self, type_, **kwargs):
        pass

    def move(self, x=0, y=0, pos=None):
        if pos:
            x, y = pos
        self.__anchor = x, y

    def set_offset_size(self, d0):
        self.__offsetSize = d0

    def scale(self, size=None, pen=None):
        if self.__offsetSize:
            self.__pen = pen

            size = self.__pen.get_size()
            self.__suf = pygame.surface.Surface(
                size[0] * self.__offsetSize[0],
                size[1] * self.__offsetSize[1]
            )

            self.__anchor = size[0] * self.__offsetRate[0] / 100, \
                            size[1] * self.__offsetRate[1] / 100

        elif size is not None:
            self.__suf = pygame.surface.Surface(size[0], size[1])

        for k, v in self.__body.items():
            v.scale(self.__suf)

    def get_size(self):
        return self.__suf.get_size()


class Grid:
    pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    spirit = Shard(screen, resManager.find())
    while 1:
        for e0 in pygame.event.get():
            if e0.type == pygame.QUIT:
                pygame.quit()
            # if e0.type not in self.legalEvents:
            #     continue
            # for i in self.listener:
            #     if e0.type in i.legalEvents:
            #         i.event(e0)
        #
        # for i in self.listener:
        #     i.update()
        screen.fill((0, 0, 0))
        # screen.blit()

        pygame.display.update()
    # Core.add(Shard())
