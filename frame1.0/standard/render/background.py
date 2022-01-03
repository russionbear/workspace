#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :background.py
# @Time      :2022/1/2 16:20
# @Author    :russionbear

"""It's just a kind map which is simple"""

from ..resource.manager import resManager
from ..core import Pen

import pygame
import sys
from ..core import Pen, Core
import pickle
import os


class BgRender:
    SCity = 0
    SRoad = 1
    SName = 2

    def __init__(self, pen, save_path):
        self.savePath = save_path
        self.pen = pen
        
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.__priImg = pygame.image.load(save_path + '/map.jpg')
        self.__img = self.__priImg.copy()
        self.__anchor = 0, 0
        self.__click = pygame.time.Clock()

        size = self.__img.get_size()
        self.__scaleList = [size]
        self.__nowScalePoint = 0
        while 1:
            if size[0] < self.__img.get_width() // 2 and \
                    size[1] < self.__img.get_height() // 2:
                break
            size = int(size[0] / 1.2), int(size[1] / 1.2)
            self.__scaleList.insert(0, size)
            self.__nowScalePoint += 1
        size = self.__img.get_size()
        while 1:
            if size[0] > self.__img.get_width() * 4 and \
                    size[1] > self.__img.get_height() * 4:
                break
            size = int(size[0] * 1.2), int(size[1] * 1.2)
            self.__scaleList.append(size)

        self.cities = []
        self.roads = []
        self.names = []

        self.__canShow = {self.SCity, self.SRoad, self.SName}

        if os.path.exists(save_path + '/points'):
            with open(save_path + '/points', 'rb') as f:
                tmp = pickle.load(f)
            # for i in tmp['cities']:
            #     self.cities.append((i[0], i[1]))
            # for i in tmp['roads']:
            #     self.cities.append((i[0], i[1]))
            self.cities = tmp['cities']
            self.roads.clear()
            for i in tmp['roads']:
                self.roads.append(tuple(i))
            self.names = tmp['names']

    def update(self):
        self.pen.blit(self.__img, self.__anchor)
        n = self.get_n()
        anchor = self.__anchor
        if self.SName in self.__canShow:
            for i in self.cities:
                pos = int(i[0] * n) + anchor[0], int(i[1] * n) + anchor[1]
                pygame.draw.circle(self.pen, (255, 0, 0), pos, 5, 5)
        elif self.SCity in self.__canShow:
            for i in self.cities:
                pos = int(i[0] * n) + anchor[0], int(i[1] * n) + anchor[1]
                pygame.draw.circle(self.pen, (255, 0, 0), pos, 5, 5)

        if self.SRoad in self.__canShow:
            for i in self.roads:
                p1, p2 = self.cities[i[0]], self.cities[i[1]]
                pos1, pos2 = (int(p1[0] * n) + anchor[0], int(p1[1] * n) + anchor[1]), \
                             (int(p2[0] * n) + anchor[0], int(p2[1] * n) + anchor[1])
                pygame.draw.line(self.pen, (0, 100, 255), pos1, pos2, 4)

    def event(self, e1):
        pass

    def move(self, y=0, x=0, pos=None):
        if pos:
            y, x = pos
        self.__anchor = y, x
        
    def get_pos(self):
        return self.__anchor
    
    def get_size(self):
        return self.__img.get_size()
    
    def get_rect(self):
        return self.__img.get_rect()

    def get_n(self):
        return self.__scaleList[self.__nowScalePoint][0] / self.__priImg.get_width()

    def get_std_size(self):
        return self.__priImg.get_size()

    def scale(self, n):
        if n > 0:
            if self.__nowScalePoint + 1 == len(self.__scaleList):
                return
            self.__nowScalePoint += 1
        else:
            if self.__nowScalePoint == 0:
                return
            self.__nowScalePoint -= 1
        size = self.__scaleList[self.__nowScalePoint]

        # self.__anchor = self.__anchor[0] + (self.__img.get_width() - size[0]) / 2, \
        #               self.__anchor[1] + (self.__img.get_height() - size[1]) / 2
        self.__img = pygame.transform.scale(self.__priImg, size)

    def save(self):
        pygame.image.save(self.get_image(), self.savePath + '\\' + 'map.png')
        tmp = {'cities': self.cities, 'roads': self.roads,
               'names': self.names, 'size': self.get_size()}
        with open(self.savePath + '/points', 'wb') as f:
            f.write(pickle.dumps(tmp))

    def clear_show(self):
        self.__canShow.clear()

    def add_show(self, t0):
        self.__canShow.add(t0)

    def get_image(self):
        return self.__img


class BgRenderEditor(BgRender):
    def __init__(self, pen, win_size, save_path, city_path):
        super(BgRenderEditor, self).__init__(pen, save_path)
        self.logs = []
        self.status = self.SCity
        self.roadB = None
        self.roadE = None

    def update(self):
        super(BgRenderEditor, self).update()
        if self.roadB is not None and self.roadE:
            anchor = self.get_pos()
            n = self.get_n()
            p1 = self.cities[self.roadB]
            pos1, pos2 = (int(p1[0] * n + anchor[0]), int(p1[1] * n) + anchor[1]), \
                         (int(self.roadE[0] * n + anchor[0]), int(self.roadE[1] * n) + anchor[1])
            pygame.draw.line(self.pen, (0, 100, 255), pos1, pos2, 4)

    def event(self, e1):
        if e1.type == pygame.MOUSEMOTION:
            if e1.buttons[0]:
                if self.status != self.SRoad:
                    return
                if self.roadB is not None:
                    p1 = self.get_pos()
                    n = self.get_n()
                    pos = (e1.pos[0] - p1[0]) / n, (e1.pos[1] - p1[1]) / n
                    self.roadE = pos

        elif e1.type == pygame.MOUSEBUTTONDOWN:
            if e1.button == 1:
                if self.status == self.SRoad:
                    self.locate_road(e1)
                elif self.status == self.SCity:
                    self.locate_city(e1)
                elif self.status == self.SName:
                    self.name_city(e1)
        elif e1.type == pygame.MOUSEBUTTONUP:
            if e1.button == 1 and self.status == self.SRoad:
                self.locate_road(e1)

    def locate_city(self, e1):
        if not self.contains(e1.pos):
            return
        p1 = self.get_pos()
        n = self.get_n()
        pos = (e1.pos[0] - p1[0]) / n, (e1.pos[1] - p1[1]) / n
        self.logs.append(self.SCity)
        self.cities.append(pos)

    def locate_road(self, e1):
        p1 = self.get_pos()
        n = self.get_n()
        pos = (e1.pos[0] - p1[0]) / n, (e1.pos[1] - p1[1]) / n
        if not self.cities:
            return
        if self.roadB is None:
            min_d = 999999
            min_c = None
            for i1, i in enumerate(self.cities):
                tmp_d = abs(((i[0] - pos[0]) ** 2 + (i[1] - pos[1]) ** 2) ** 0.5)
                if tmp_d < min_d:
                    min_c = i1
                    min_d = tmp_d
            self.roadB = min_c

        else:
            min_d = 999999
            min_c = None
            for i1, i in enumerate(self.cities):
                tmp_d = abs(((i[0] - pos[0]) ** 2 + (i[1] - pos[1]) ** 2) ** 0.5)
                if tmp_d < min_d:
                    min_c = i1
                    min_d = tmp_d
            if (self.roadB, min_c) in self.roads or \
                    (min_c, self.roadB) in self.roads or\
                    min_c == self.roadB or min_c is None:
                pass
            else:
                self.roads.append((self.roadB, min_c))
                self.logs.append(self.SRoad)
            self.roadB = self.roadE = None

    def name_city(self, e1):
        pass

    def clear_log(self):
        if not self.logs:
            return
        t0 = self.logs.pop()
        if t0 == self.SCity:
            self.cities.pop()
        elif t0 == self.SRoad:
            self.roads.pop()
        elif t0 == self.SName:
            self.names.pop()

    def save(self):
        pygame.image.save(self.get_image(), self.savePath+'\\'+'map.jpg')
        tmp = {'cities': self.cities, 'roads': self.roads}
        with open(self.savePath+'/points', 'wb') as f:
            f.write(pickle.dumps(tmp))

    def contains(self, pos):
        p1 = self.get_pos()
        return self.get_rect().move(p1[0], p1[1]).collidepoint(pos[0], pos[1])

    def swap_status(self):
        self.status = (self.status + 1) % (self.SName + 1)


class Tool:
    City = 1
    Road = 2

    def __init__(self, size):
        self.suf = pygame.display.set_mode(size)
        self.legalEvents = {pygame.MOUSEBUTTONDOWN}
        self.nowP = 0
        self.city = {'suf': Pen.render('asdasd'), 'anchor': (0, 0), 'rect': None}
        self.road = {'suf': Pen.render('dasdasd'), 'anchor': (100, 0), 'rect': None}

    def update(self):
        self.city['rect'] = self.suf.blit(self.city['suf'], self.city['anchor'])
        if self.nowP == self.City:
            pygame.draw.rect(self.suf, pygame.color.Color(255, 0, 0), self.city['rect'], width=5)
        self.road['rect'] = self.suf.blit(self.road['suf'], self.road['anchor'])
        if self.nowP == self.Road:
            pygame.draw.rect(self.suf, pygame.color.Color(255, 0, 0), self.road['rect'], width=5)

    def event(self, e1):
        if e1.button != 1:
            return
        if self.city['rect']:
            if self.city['rect'].collidepoint(e1.pos):
                self.nowP = self.City
                return
        if self.city['rect']:
            if self.road['rect'].collidepoint(e1.pos):
                self.nowP = self.Road


class ListView:
    def __init__(self, pen, size, data):
        self.__data: list = data
        self.__pen = pen
        self.__suf = pygame.surface.Surface(size)
        self.__bgColor = (0, 0, 0)

        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.__anchor = 0, 0

        self.__rows = self.__suf.get_height() // Pen.get_font_size()
        self.__blockHeight = Pen.get_font_size()
        self.__cols = 1
        self.__blockWidth = 1
        self.__point = 0
        self.__chose = 0
        self.scroll(False)
        self.scroll(True)

    def update(self):
        self.__pen.blit(self.__suf, self.__anchor)
        self.__suf.fill(self.__bgColor)
        up = self.__cols * self.__rows
        for i1, i in enumerate(self.__data[self.__point:up+self.__point]):
            rect = self.__suf.blit(Pen.render(i),
                            (i1 % self.__cols * self.__blockWidth + self.__anchor[0],
                             i1 // self.__cols * self.__blockHeight + self.__anchor[1])
                            )
            if self.__point + i1 == self.__chose:
                pygame.draw.rect(self.__suf, (100, 200, 0), rect, 4)

    def event(self, e1):
        if e1.type == pygame.MOUSEBUTTONDOWN:
            if e1.button == 1:
                pos = e1.pos[0] - self.__anchor[0], \
                    e1.pos[1] - self.__anchor[1]
                xy = pos[0] // self.__blockWidth, pos[1] // self.__blockHeight
                if xy[0] + xy[1] * self.__cols + self.__point >= len(self.__data):
                    return
                if xy[0] < 0 or xy[1] < 0:
                    return
                self.__chose = xy[0] + xy[1] * self.__cols + self.__point

            elif e1.button == 4:
                self.scroll(True)
            elif e1.button == 5:
                self.scroll()

    def move(self, y=0, x=0, pos=None):
        if pos:
            y, x = pos
        self.__anchor = y, x

    def scroll(self, up=False):
        v = self.__cols * self.__rows
        if up:
            self.__point -= self.__cols
            if self.__point < 0:
                self.__point = 0
        else:
            if len(self.__data) <= v:
                return
            self.__point += self.__cols
            if self.__point + v > len(self.__data):
                self.__point = len(self.__data) - v

            # vc = len(self.__data) % v
            # vq = len(self.__data) // v * v
            # self.__point += self.__cols
            # if vc == 0:
            #     if self.__point >= vq:
            #         self.__point = vq - v
            #
            #     print('00')
            # else:
            #     if self.__point >= vq:
            #         self.__point = vq

            # print(self.__point, vq, len(self.__data))

        self.__blockWidth = 0
        for i1, i in enumerate(self.__data[self.__point:v]):
            rect = self.__suf.blit(Pen.render(i), (0, 0))
            self.__blockWidth = max(rect.width, self.__blockWidth)
        self.__blockWidth += 7
        self.__cols = self.__suf.get_width() // self.__blockWidth

    def get_chose(self):
        return self.__data[self.__chose]

    def get_pos(self):
        return self.__anchor

    def get_size(self):
        return self.__suf.get_size()

    def get_rect(self):
        return self.__suf.get_rect()

    def insert(self, value, cursor=None):
        if cursor is None:
            self.__data.append(value)
        else:
            self.__data.insert(cursor, value)

    def remove(self, value):
        self.__data.remove(value)

    def pop(self, index=-1):
        if self.__data:
            return self.__data.pop(index)


class BgRenderShow(BgRender):
    def __init__(self, save_path, win_size):
        super(BgRenderShow, self).__init__(save_path, win_size)


class TestWin:
    def __init__(self):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.suf = pygame.display.set_mode(size)

        self.isCtrlDown = False

    def update(self):
        self.suf.fill((0, 0, 0))

    def event(self, e0):
        if e0.type == pygame.MOUSEMOTION:
            if e0.buttons[2]:
                pos = self.render.get_pos()
                pos = pos[0] + e0.rel[0], pos[1] + e0.rel[1]
                self.render.move(pos=pos)
            elif e0.buttons[0]:
                self.render.event(e0)

        if e0.type == pygame.MOUSEBUTTONDOWN:
            pygame.event.set_grab(True)
            if e0.button == 1:
                self.render.event(e0)
            elif e0.button == 4 or e0.button == 5:
                p0 = self.render.get_pos()
                anchor1 = p0[0] - self.__winAnchor[0], \
                          p0[1] - self.__winAnchor[1]
                n1 = self.render.get_n()
                self.render.scale(int(not bool(e0.button-4)))

                n2 = self.render.get_n()
                n = n2 / n1
                d0 = int(n*anchor1[0]) + self.__winAnchor[0], \
                     int(n*anchor1[1]) + self.__winAnchor[1]
                self.render.move(pos=d0)

        elif e0.type == pygame.MOUSEBUTTONUP:
            pygame.event.set_grab(False)
            if e0.button == 1:
                self.render.event(e0)

        elif e0.type == pygame.KEYDOWN:
            if e0.key == pygame.K_LCTRL:
                self.isCtrlDown = True
            elif e0.key == pygame.K_z and self.isCtrlDown:
                self.render.clear_log()
            elif e0.key == pygame.K_s and self.isCtrlDown:
                self.render.save()
            elif e0.key == pygame.K_TAB:
                self.render.swap_status()
        elif e0.type == pygame.KEYUP:
            if e0.key == pygame.K_LCTRL:
                self.isCtrlDown = False

    def clear_log(self):
        for i in range(1, len(self.points)):
            if self.points[-i] is None:
                self.points = self.points[:-i]
                return


class TestWinEditor:
    def __init__(self, size, save_path, city_path):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.suf = pygame.display.set_mode(size)

        self.render = BgRenderEditor(self.suf, save_path)

        self.__winAnchor = self.suf.get_width()//2, self.suf.get_height()//2
        self.isMouseDown = False
        self.isCtrlDown = False

        with open(city_path, 'r', encoding='utf-8') as f:
            s0 = f.read()
        self.tool = ListView(self.pen, win_size, s0.split('\n'))
        self.toolShowed = False

    def update(self):
        self.suf.fill((0, 0, 0))
        if self.toolShowed:
            self.tool.update()
            return
        self.render.update()
        self.suf.blit(Pen.render(str(self.render.status)), (0, 0))

    def event(self, e0):
        if e0.type == pygame.MOUSEMOTION:
            if e0.buttons[2]:
                pos = self.render.get_pos()
                pos = pos[0] + e0.rel[0], pos[1] + e0.rel[1]
                self.render.move(pos=pos)
            elif e0.buttons[0]:
                self.render.event(e0)

        if e0.type == pygame.MOUSEBUTTONDOWN:
            pygame.event.set_grab(True)
            if e0.button in (1, 4, 5) and self.toolShowed:
                self.tool.event(e0)
                return

            if e0.button == 1:
                self.render.event(e0)
            elif e0.button == 4 or e0.button == 5:
                p0 = self.render.get_pos()
                anchor1 = p0[0] - self.__winAnchor[0], \
                          p0[1] - self.__winAnchor[1]
                n1 = self.render.get_n()
                self.render.scale(int(not bool(e0.button-4)))

                n2 = self.render.get_n()
                n = n2 / n1
                d0 = int(n*anchor1[0]) + self.__winAnchor[0], \
                     int(n*anchor1[1]) + self.__winAnchor[1]
                self.render.move(pos=d0)

        elif e0.type == pygame.MOUSEBUTTONUP:
            pygame.event.set_grab(False)
            if e0.button == 1:
                self.render.event(e0)

        elif e0.type == pygame.KEYDOWN:
            if e0.key == pygame.K_LCTRL:
                self.isCtrlDown = True
            elif e0.key == pygame.K_z and self.isCtrlDown:
                self.render.clear_log()
            elif e0.key == pygame.K_s and self.isCtrlDown:
                self.render.save()
            elif e0.key == pygame.K_TAB:
                if self.isCtrlDown:
                    self.toolShowed = not self.toolShowed
                else:
                    self.render.swap_status()
        elif e0.type == pygame.KEYUP:
            if e0.key == pygame.K_LCTRL:
                self.isCtrlDown = False


class TestWinTool:
    def __init__(self, size):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.suf = pygame.display.set_mode(size)

        self.render = ListView(self.suf, size, ['1'])

        self.isCtrlDown = False

    def update(self):
        self.suf.fill((0, 0, 0))
        self.render.update()

    def event(self, e0):
        if e0.type == pygame.MOUSEBUTTONDOWN:
            if e0.button == 1:
                self.render.event(e0)
            elif e0.button == 4 or e0.button == 5:
                self.render.event(e0)

