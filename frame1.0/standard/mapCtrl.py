#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :mapCtrl.py
# @Time      :2021/12/31 13:06
# @Author    :russionbear


from typing import Dict, List
from .resource import UnitMaker, resManager, Spirit, UnitLoader
from .core import Core, Pen

import pygame, os, json


# resManager = ResMngMaker.init('mode')


class MapRender:
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

        # self.chose = None

        # self.circleStart: tuple | ... = None
        # self.circleRect: pygame.rect.Rect | ... = None
        # self.circleLog = None

        # UnitMaker.make(['unit', 'red', 'bigman']).copy()

    def init_map(self, size, bg, border):
        self.basicLayer = [[None for i in range(size[0])] for j in range(size[1])]
        self.mapRl = size
        self.border = border
        self.suf = pygame.surface.Surface((size[0] * self.blockSize[0],
                                           size[1] * self.blockSize[1]))
        if bg:
            self.backGround = UnitMaker.make(bg)
            self.backGround.set_pen(self.pen)

    def load_map(self, path):
        with open(path, 'r') as f:
            tmp_d = json.load(f)
        if tmp_d['background'] is not None:
            self.backGround = UnitMaker.make(tmp_d['background'])
            self.backGround.set_pen(self.pen)
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

        self.scale(-1)

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
            self.pen.blit(self.suf, self.anchor)
        else:
            self.pen.blit(self.suf, self.anchor)
            self.suf.fill((255, 255, 255))

        for r in self.basicLayer:
            for l in r:
                if l:
                    l.update(t0)

        for k, v in self.spirits.items():
            for k1 in list(v.values()):
                k1.update(t0)

        return t0

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
                j.move(size[0] * j1, size[1] * i1)

        for k, v in self.spirits.items():
            for k1, v1 in v.items():
                v1.scale(self.suf, size)
                v1.move(size[0] * k1[0], size[1] * k1[1])

        # bw, bh = size[0] // self.mapRl[0], size[1] // self.mapRl[1]
        # for i1, i in enumerate(self.map):
        #     for j1, j in enumerate(i):
        #         j.scale((bw, bh))
        #         j.move(j1*bw, i1*bh)

    def event(self, e1):
        pass


class MapEditRender(MapRender):
    def __init__(self, pen: pygame.surface.Surface, block_size):
        super(MapEditRender, self).__init__(pen, block_size)
        self.chose = None

        self.circleStart: tuple | ... = None
        self.circleRect: pygame.rect.Rect | ... = None
        self.circleLog = None

    def init_map(self, size, bg, border):
        super(MapEditRender, self).init_map(size, bg, border)

    def load_map(self, path):
        super(MapEditRender, self).load_map(path)

        self.scale(-1)

    def to_sequence(self):
        return super(MapEditRender, self).to_sequence()

    def update(self):
        super(MapEditRender, self).update()

        if self.circleRect is not None:
            pygame.draw.rect(self.suf, (0, 255, 100), self.circleRect, 5)

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
                x2, y2 = (x + w) // block_size[0] + 1, (y + h) // block_size[1] + 1

                print(x1, x2, y1, y2, x, y)
                self.cover(x1, x2, y1, y2)

                self.circleStart = None
                self.circleRect = None

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


class MapShowRender(MapRender):
    def __init__(self, pen, size):
        super(MapShowRender, self).__init__(pen, size)
        self.motor = Motor()

    def update(self):
        self.motor.update(super(MapShowRender, self).update())

    def get(self, layer, x=0, y=0, pos=None) -> Spirit:
        if pos is not None:
            x, y = pos
        if layer == 1:
            return self.basicLayer[y][x]
        if layer in self.spirits:
            if (x, y) in self.spirits[layer]:
                return self.spirits[layer][(x, y)]


class MapMenu:
    pass


class Motor:
    Delay = 0
    Action = 1
    Move = 2

    def __init__(self):
        self.__data = {}

    def add(self, obj, cmd):
        self.__data[obj] = cmd

    def remove(self, obj):
        if obj in self.__data:
            del self.__data[obj]

    def update(self, t0):
        should_d = set()
        for k, v in self.__data.items():
            tmp = v[0]
            if tmp[0] == self.Action:
                k.swap(tmp[2], tmp[1])
                v.pop(0)
            elif tmp[0] == self.Delay:
                tmp[1] -= t0
                if tmp[1] <= 0:
                    v.pop(0)
            elif tmp[0] == self.Move:
                if self.move(k, tmp[1], tmp[2]):
                    v.pop(0)
            if not v:
                should_d.add(k)
        for i in should_d:
            del self.__data[i]

    @staticmethod
    def move(obj: Spirit, rl, step):
        pos1 = obj.get_pos()
        size = obj.get_size()
        target = size[0] * rl[0], size[1] * rl[1]
        d1 = target[0] - pos1[0], target[0] - pos1[1]
        distance = (d1[0] ** 2 + d1[1] ** 2) ** 0.5
        step = step * size[0] / 100
        if distance <= step:
            obj.move(pos=target)
            return True
        else:
            n = step / distance
            d1 = int(d1[0] * n) + pos1[0], int(d1[1] * n) + pos1[1]
            obj.move(pos=d1)
            return False


class Scientist:
    @staticmethod
    def aaa():
        pass
