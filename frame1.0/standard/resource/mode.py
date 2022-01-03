#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :mode.py
# @Time      :2022/1/2 15:42
# @Author    :russionbear

import pygame, copy

"""mode"""


class Mode:
    def __init__(self, it):
        self.__body = next(it)
        self.__firstAction = tuple(next(it))

        rect = next(it)
        self.__collideRect = pygame.rect.Rect(rect[0], rect[1], rect[2], rect[3])
        self.__miniColor = tuple(next(it))

        self.__interface = next(it)

        self.__actions = next(it)

    def get_action(self, name, type_):
        if '' in self.__actions[type_]:
            return self.__actions[type_]['']
        return self.__actions[type_][name].copy()

    def get_body(self):
        return self.__body.copy()

    def get_first_action(self):
        return self.__firstAction

    def get_all_actions(self):
        rlt = []
        for k, v in self.__actions.items():
            for k1, v1 in v.items():
                rlt.append((k, k1))
        return rlt

    def copy(self):
        print('fdfrrr')
        rect = self.__collideRect
        self.__collideRect = None
        obj = copy.copy(self)
        # obj.rect = rect.copy()
        self.__collideRect = rect
        return obj

    def to_json(self):
        rlt = {}
        for k, v in self.__actions.items():
            for k1, v1 in v.items():
                if 'layer' not in v1:
                    continue
                layers = v1['layer']
                rate = []
                size = []
                for p in layers:
                    rate.append(v1['offset_rate'][p])
                    size.append(v1['offset_size'][p])
                rlt['-'.join(['action', k, k1])] = {
                    "layer": layers,
                    "offset_rate": rate,
                    "offset_size": size
                }
        return rlt

    def is_interface(self):
        return self.__interface

    def get_index(self):
        return {}

    def get_flag(self):
        pass

    # def contains(self, pos):
    #     return


class ModeA(Mode):
    def __init__(self, data):
        it = iter(data)
        self.usage = next(it)
        self.flag = next(it)
        self.name = next(it)

        super(ModeA, self).__init__(it)

    def get_index(self):
        return [self.usage, self.flag, self.name]

    def get_flag(self):
        return self.flag


class ModeMaker:
    @staticmethod
    def make(data):
        return ModeA(data)

