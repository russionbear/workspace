#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :unit.py
# @Time      :2022/1/2 15:42
# @Author    :russionbear

from __future__ import print_function
from .source import Source
from .manager import resManager
from .setting import STUnit

from typing import Dict
import pygame
import copy


"""unit"""
# 第一层unit 是必须的


class Shard:
    def __init__(self,
                 source: Source,
                 pen: pygame.surface.Surface = None):
        self.__pen = pen
        # 100
        self.__offsetRate = 0, 0
        self.__offsetSize = 0, 0
        self.__anchor = 0, 0
        self.__source = source

    def set_pen(self, pen):
        self.__pen = pen

    def swap(self, name, type_=None):
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
        self.scale(self.__pen)

    def set_offset_rate(self, d0):
        self.__offsetRate = d0
        self.scale(self.__pen)

    def get_offset_rate(self):
        return self.__offsetRate

    def get_offset_size(self):
        return self.__offsetSize

    def scale(self, pen):
        size = pen.get_size()
        self.__source.scale_to((size[0] * self.__offsetSize[0] / 100,
                                size[1] * self.__offsetSize[1] / 100
                                ))
        self.__anchor = size[0] * self.__offsetRate[0] / 100, \
                        size[1] * self.__offsetRate[1] / 100

        self.__pen = pen

    def get_rect(self):
        return self.__source.get_rect()

    def get_size(self):
        return self.__source.get_size()

    def get_pos(self):
        return self.__anchor

    # def get_anchor(self):
    #     return self.__anchor

    def contains(self, pos):
        pos = pos[0] - self.__anchor[0], pos[1] - self.__anchor[1]
        return self.__source.contains(pos)

    def copy(self, pen_):
        pen = self.__pen
        self.__pen = None
        obj = copy.copy(self)
        self.__pen = pen
        obj.set_pen(pen_)
        return obj


class Spirit:
    def __init__(self, obj, pen=None, top=True, layer=1):
        self.__pen = pen
        self.__suf = pygame.surface.Surface(resManager.blockSize)
        # 100
        self.__offsetRate = (0, 0) if not top else None
        self.__offsetSize = (0, 0) if not top else None
        self.__anchor = 0, 0

        self.__source = obj
        self.__body: Dict[str, ...] = {}
        for k, v in obj.get_body().items():
            self.__body[k] = v.copy(self.__suf)
            # self.__body[k].set_pen(self.s)

        self.__action = {}
        # self.__collideRect = 0, 0, 0, 0
        self.__renderOrder: list = []
        self.__nowAction = None

        self.__layer = layer

        self.swap(obj.get_first_action()[1], obj.get_first_action()[0])

    def swap(self, name, type_=None):
        self.__nowAction = type_, name
        action = self.__source.get_action(name, type_)
        if 'layer' in action:
            self.__renderOrder = action['layer']
            for i in self.__renderOrder:
                self.__body[i].move(pos=action['offset_rate'][i])
                self.__body[i].set_offset_size(action['offset_size'][i])
        if 'to' in action:
            for k in action['to']:
                self.__body[k].swap(name, type_)
        self.__action[type_] = name

    def update(self, t0):
        # print(self.__dict__)
        if self.__pen:
            self.__pen.blit(self.__suf, self.__anchor)
            self.__suf.fill((0, 50, 0))
            for i in self.__renderOrder:
                self.__body[i].update(t0)
                # print('update')

    def slots(self, type_, **kwargs):
        pass

    def move(self, x=0, y=0, pos=None):
        if pos:
            x, y = pos
        self.__anchor = x, y

    def set_offset_size(self, d0):
        if self.__pen:
            self.__offsetSize = d0
            self.scale()

    def set_offset_rate(self, d0):
        if self.__pen:
            self.__offsetRate = d0
            self.scale()

    def get_offset_rate(self):
        return self.__offsetRate

    def get_offset_size(self):
        return self.__offsetSize

    def scale(self, pen=None, size=None):
        if pen is not None:
            self.set_pen(pen)

        if self.__offsetSize is not None:
            print(self.__offsetSize, 'not top')

            size = self.__pen.get_size()
            self.__suf = pygame.surface.Surface(
                size[0] * self.__offsetSize[0] // 100,
                size[1] * self.__offsetSize[1] // 100
            )

            self.__anchor = size[0] * self.__offsetRate[0] / 100, \
                size[1] * self.__offsetRate[1] / 100

        else:
            self.__suf = pygame.surface.Surface((int(size[0]), int(size[1])))

        for k, v in self.__body.items():
            v.scale(self.__suf)

    def get_rect(self):
        return self.__suf.get_rect()

    def get_size(self):
        return self.__suf.get_size()

    def get_pos(self):
        return self.__anchor

    def get_all_actions(self):
        return self.__source.get_all_actions()

    def get_layer(self):
        return self.__layer

    def get_flag(self):
        return self.__source.get_flag()

    def set_pen(self, pen):
        self.__pen = pen

    def copy(self):
        suf = self.__suf
        body = self.__body
        self.__suf = None
        self.__body = None

        obj = copy.copy(self)

        obj.__suf = suf.copy()
        self.__suf = suf
        obj.__body = {}
        for k, v in body.items():
            obj.__body[k] = v.copy(obj.__suf)
        self.__body = body
        obj.__pen = None
        obj.__action = obj.__action.copy()
        return obj

    def contains(self, pos):
        pos = pos[0] - self.__anchor[0], pos[1] - self.__anchor[1]
        return self.__suf.get_rect().collidepoint(pos[0], pos[1])

    def collide_point(self, pos):
        if self.contains(pos):
            pos = pos[0] - self.__anchor[0], pos[1] - self.__anchor[1]
            for k in reversed(self.__renderOrder):
                if self.__body[k].contains(pos):
                    return self.__body[k]

    def to_json(self):
        tmp_d = self.__source.to_json()
        for k, v in tmp_d.items():
            if 'layer' not in v:
                continue
            if '-'.join(['action', self.__nowAction[0], self.__nowAction[1]]) == k:
                for i1, i in enumerate(self.__renderOrder):
                    tmp_d[k]['offset_rate'][i1] = self.__body[i].get_offset_rate()
                    tmp_d[k]['offset_size'][i1] = self.__body[i].get_offset_size()
        print(tmp_d)
        return tmp_d

    def to_sequence(self):
        tmp_k = {
                 'now_action': self.__nowAction,
                 'action': self.__action,
                 'track': self.__source.get_index()
                 }
        return tmp_k

    def init_by_sequence(self, sq, pen):
        self.__nowAction = sq['now_action']
        self.__action = sq['action']
        self.__pen = pen


class Grid:
    pass


class UGeo(Spirit):
    def __init__(self, mode, pen):
        super(UGeo, self).__init__(mode, pen)
        self.geo = STUnit.get_key(mode.get_index(), 're_geo')

    def get_geo(self):
        return self.geo

    # def get_geo(self):
    #     return self.geo


class UBuild(Spirit):
    def __init__(self, mode, pen):
        super(UBuild, self).__init__(mode, pen, layer=2)


class UUnit(Spirit):

    def __init__(self, mode, pen):
        super(UUnit, self).__init__(mode, pen, layer=3)

        index = mode.get_index()
        self.body = 10
        self.foot = STUnit.get_key(index, 're_foot')
        self.eye = STUnit.get_key(index, 're_eye')
        self.atk = STUnit.get_key(index, 're_atk')
        self.bullet = STUnit.get_key(index, 'v_top_bullet')
        self.oil = STUnit.get_key(index, 'v_top_oil')

        self.convey = STUnit.get_key(index, 'convey')

        self.restStep = STUnit.get_key(index, 'v_day_cost')
        self.isMoved = True


class UnitMaker:
    @staticmethod
    def make(data):
        obj = resManager.get(args=data)
        print(obj, data)
        if obj is None:
            raise OSError
        return Spirit(obj)


class UnitLoader:
    @staticmethod
    def load(sq, pen):
        obj = resManager.get(args=sq['track'])
        if obj is None:
            raise OSError
        obj = Spirit(obj)
        obj.init_by_sequence(sq, pen)
        return obj

