#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :source.py
# @Time      :2022/1/2 15:42
# @Author    :russionbear

from __future__ import print_function
from .manager import resManager

import pygame
import copy


class Source:
    def __init__(self, it):
        self.__index = list(self.__dict__.keys())

        self.__boss = resManager
        self.__id = 0
        self.__sound = ''
        self.__priImages = []
        self.__images = []
        self.__nowPoint = 0
        self.__nowImage = None

        self.__gap = 0
        self.__nowTime = 0.0

        self.__init(it)

    def __init(self, it):
        self.__id = next(it)
        self.__sound = next(it)
        self.__priImages = next(it)
        self.__images = self.__priImages[:]
        self.__nowPoint = 0
        self.__nowImage = self.__images[0]

        self.__gap = next(it)
        self.__nowTime = 0.0

    def make_it(self):
        return iter([self.__id, self.__sound, self.__priImages, self.__gap])

    def scale(self, rate):
        size_ = self.__priImages[0].get_size
        size = int(size_[0] * rate), int(size_[1] * rate)

        for i1, i in enumerate(self.__priImages):
            self.__images[i1] = pygame.transform.scale(i, size)
        self.__nowImage = self.__images[self.__nowPoint]

    def scale_to(self, size):
        size = int(size[0]), int(size[1])
        for i1, i in enumerate(self.__priImages):
            self.__images[i1] = pygame.transform.scale(i, size)
        self.__nowImage = self.__images[self.__nowPoint]

    def get(self):
        return self.__nowImage

    def update(self, t0):
        self.__nowTime += t0
        if self.__nowTime > self.__gap:
            self.__nowTime = 0.0
            self.__nowPoint = (self.__nowPoint + 1) % len(self.__images)
            self.__nowImage = self.__images[self.__nowPoint]

    def swap(self, name):
        size = self.__nowImage.get_size()
        setattr(self, self.__index[-1], name)
        self.__init(
            self.__boss.find(
                args=self.get_index()
            ).make_it())

        self.scale(size)

    def play(self):
        if self.__sound is not None:
            pygame.mixer.Sound(self.__sound).play(1)

    def get_size(self):
        return self.__nowImage.get_size()

    def get_rect(self):
        return self.__nowImage.get_rect()

    def copy(self):
        obj = copy.copy(self)
        obj.__images = obj.__images.copy()
        obj.__nowImage = obj.__images[0]
        return obj

    def get_id(self):
        return self.__id

    def contains(self, pos):
        return self.__nowImage.get_rect().collidepoint(pos[0], pos[1])

    def get_index_key(self):
        return self.__index

    def get_index(self):
        return [getattr(self, i) for i in self.__index]


class SGround(Source):
    def __init__(self, data):
        it = iter(data)
        self.usage: str = it.__next__()
        self.name: str = it.__next__()
        self.action: str = it.__next__()
        super(SGround, self).__init__(it)
        # self.layer = 0


class SUnit(Source):
    def __init__(self, data):
        it = iter(data)
        self.usage: str = it.__next__()
        self.flag: str = it.__next__()
        self.name: str = it.__next__()
        self.action: str = it.__next__()
        super(SUnit, self).__init__(it)


class STag(Source):
    def __init__(self, data):
        it = iter(data)
        self.usage: str = it.__next__()
        self.name: str = it.__next__()
        self.action: str = it.__next__()
        super(STag, self).__init__(it)


class SourceMaker:
    @staticmethod
    def make(l0):
        """

        :param l0:
        :return: TrackBasic, TrackUnit
        """
        if l0[0] == 'geo':
            return SGround(l0)
        elif l0[0] == 'unit':
            return SUnit(l0)
        elif l0[0] == 'tag':
            return STag(l0)

