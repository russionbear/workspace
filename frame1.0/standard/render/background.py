#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :background.py
# @Time      :2022/1/2 16:20
# @Author    :russionbear

"""It's just a kind map which is simple"""

from ..resource.manager import resManager
from ..core import Pen, Core
from .ui.listView import ListView

import pygame
import sys
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

        self.cities = []
        self.roads = []
        self.names = {}

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

            block_size = tmp['size']
            self.__img = pygame.transform.scale(self.__priImg, block_size)

        size = self.__img.get_size()
        self.__scaleList = [size]
        self.__nowScalePoint = 0
        while 1:
            if size[0] < self.pen.get_width() and \
                    size[1] < self.pen.get_height():
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

    def update(self):
        self.pen.blit(self.__img, self.__anchor)
        n = self.get_n()
        anchor = self.__anchor
        font_size = Pen.get_font_size()
        if self.SName in self.__canShow:
            for i1, i in enumerate(self.cities):
                pos = int(i[0] * n) + anchor[0], int(i[1] * n) + anchor[1]
                pygame.draw.circle(self.pen, (255, 0, 0), pos, 5, 5)
                if i1 in self.names:
                    self.pen.blit(Pen.render(self.names[i1]),
                                  (pos[0]-Pen.get_width(self.names[i1])//2,
                                   pos[1]-font_size//2)
                                  )
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

    def move(self, x=0, y=0, pos=None):
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

    def clear_log(self):
        if not self.logs:
            return
        t0 = self.logs.pop()
        if t0 == self.SCity:
            self.cities.pop()
        elif t0 == self.SRoad:
            self.roads.pop()
        else:
            return t0
        # elif t0 == self.SName:
        #     self.names.pop()


class BgRenderEditor(BgRender):
    def __init__(self, pen, win_size, save_path):
        super(BgRenderEditor, self).__init__(pen, save_path)
        self.logs = []
        self.status = self.SCity
        self.roadB = None
        self.roadE = None
        self.__targetTo = None

    def set_target_to(self, obj):
        self.__targetTo = obj

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
        p1 = self.get_pos()
        n = self.get_n()
        pos = (e1.pos[0] - p1[0]) / n, (e1.pos[1] - p1[1]) / n
        if not self.cities:
            return

        name = self.__targetTo.get_name()
        if name is None:
            return

        min_d = 999999
        min_c = None
        for i1, i in enumerate(self.cities):
            tmp_d = abs(((i[0] - pos[0]) ** 2 + (i[1] - pos[1]) ** 2) ** 0.5)
            if tmp_d < min_d:
                min_c = i1
                min_d = tmp_d
        should_d = []
        for k, v in self.names.items():
            if v == name:
                should_d.append(k)
        for i in should_d:
            del self.names[i]
        if min_c in self.names:
            name_ = self.names[min_c]
            self.names[min_c] = name
            self.__targetTo.del_name()
            self.__targetTo.add_name(name_)
        else:
            self.names[min_c] = name
            self.__targetTo.del_name()
        self.logs.append((min_c, 0))

    def contains(self, pos):
        p1 = self.get_pos()
        return self.get_rect().move(p1[0], p1[1]).collidepoint(pos[0], pos[1])

    def swap_status(self):
        self.status = (self.status + 1) % (self.SName + 1)

    def clear_log(self):
        t0 = super(BgRenderEditor, self).clear_log()
        if isinstance(t0, tuple):
            print(t0)
            self.__targetTo.add_name(self.names[t0[0]])
            del self.names[t0[0]]


class BgRenderShow(BgRender):
    def __init__(self, pen, save_path):
        super(BgRenderShow, self).__init__(pen, save_path)
        self.__click = pygame.time.Clock()
        self.motor = Motor()
        self.moveDirection = None
        self.moveTarget = None

        n = 0
        while 1:
            size = self.get_size()
            super(BgRenderShow, self).scale(-1)
            if size == self.get_size():
                break
            n += 1

        self.nowScaleStd = n
        self.isMiniMap = True

        self.cityBelong = {}

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

            block_size = tmp['size']
            self.__img = pygame.transform.scale(self.__priImg, block_size)

    def update(self):
        super(BgRenderShow, self).update()
        self.motor.update(self.__click.get_time())
        if self.moveDirection is not None:
            pos = self.get_pos()
            modified = self.move(x=pos[0]+self.moveDirection[0], y=pos[1]+self.moveDirection[1])
            x, y = self.moveDirection
            if modified == 0:
                return
            elif modified == 3:
                x = y = 0
            else:
                if x != 0 and modified == 1:
                    x = 0
                if y != 0 and modified == 2:
                    y = 0
            if x == 0 and y == 0:
                self.moveDirection = None
            else:
                self.moveDirection = x, y

        elif self.moveTarget:
            self.auto_move()

        # elif self.scaleTarget

    def move(self, x=0, y=0, pos=None):
        size = self.get_size()
        p_size = self.pen.get_size()
        if pos is not None:
            x, y = pos

        modified = 0

        if p_size[0] >= size[0]:
            x = (p_size[0]-size[0]) // 2
        else:
            if x > 0:
                x = 0
                modified += 1
            elif x + size[0] < p_size[0]:
                x = p_size[0] - size[0]
                modified += 1

        if p_size[1] >= size[1]:
            y = (p_size[1]-size[1]) // 2
        else:
            if y > 0:
                y = 0
                modified += 2
            elif y + size[1] < p_size[1]:
                y = p_size[1] - size[1]
                modified += 2

        super(BgRenderShow, self).move(y=x, x=y)
        # print(modified, 'm')
        return modified

    def scale(self, n):
        if n > 0 and self.isMiniMap:
            for i in range(self.nowScaleStd):
                super(BgRenderShow, self).scale(1)
            self.isMiniMap = False
        elif not self.isMiniMap:
            for i in range(self.nowScaleStd):
                super(BgRenderShow, self).scale(-1)
            self.isMiniMap = True

    def event(self, e1):
        if e1.type == pygame.MOUSEMOTION:
            pass

    def set_move_direction(self, xy=None):
        # return
        self.moveDirection = xy

    def auto_move(self):
        p1 = self.get_pos()
        pos = self.moveTarget
        step = 1
        d1 = pos[0] - p1[0], pos[1] - p1[1]
        distance = (d1[0] ** 2 + d1[1] ** 2) ** 0.5
        if distance < step:
            self.move(pos=pos)
            self.moveTarget = None
        n = step / distance

        x, y = int(d1[0] * n), int(d1[1] * n)
        x = x if x else 1 if d1[0] > 0 else -1
        y = y if y else 1 if d1[1] > 0 else -1

        p2 = p1[0] + x, p1[1] + y

        if self.move(pos=p2) != 0:
            self.moveTarget = None

    def save(self):
        if self.isMiniMap:
            self.scale(1)
        super(BgRenderShow, self).save()

    def swap_names(self, names):
        self.names = names


class Motor:
    Delay = 0
    Action = 1
    Move = 2
    Scale = 3

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
    def move(obj: BgRender, pos, step):
        p1 = obj.get_pos()
        d1 = pos[0] - p1[0], pos[1] - p1[1]
        distance = (d1[0] ** 2 + d1[1] ** 2) ** 0.5
        if distance < step:
            obj.move(pos=pos)
            return True
        n = step / distance
        p2 = p1[0] + int(d1[0] * n), p1[1] + int(d1[1] * n)
        obj.move(pos=p2)

    @staticmethod
    def scale(obj: BgRender, n):
        while n > 0:
            obj.scale(1)
            n -= 1
        while n < 0:
            obj.scale(-1)
            n += 1


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
    def __init__(self, size, save_path, city_path=None):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.suf = pygame.display.set_mode(size)

        self.render = BgRenderEditor(self.suf, size, save_path)
        self.render.set_target_to(self)

        self.__winAnchor = self.suf.get_width()//2, self.suf.get_height()//2
        self.isMouseDown = False
        self.isCtrlDown = False

        """此方案略微复杂 <875690>"""
        # with open(city_path, 'r', encoding='utf-8') as f:
        #     s0 = f.read()
        # self.tool = ListView(self.pen, win_size, s0.split('\n'))
        # self.toolShowed = False

        self.storageName = ['name']
        self.pointName = 0
        if city_path:
            with open(city_path, 'r', encoding='utf-8') as f:
                s0 = f.read()
            self.storageName = s0.split('\n')

    def update(self):
        self.suf.fill((0, 0, 0))
        """875690"""
        # if self.toolShowed:
        #     self.tool.update()
        #     return
        self.render.update()
        self.suf.blit(Pen.render(str(self.render.status)), (0, 0))
        if self.storageName[self.pointName]:
            self.suf.blit(Pen.render(self.storageName[self.pointName]), (30, 0))

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
            """875690"""
            # if e0.button in (1, 4, 5) and self.toolShowed:
            #     self.tool.event(e0)
            #     return

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
                    """875690"""
                    # self.toolShowed = not self.toolShowed
                    pass
                else:
                    self.render.swap_status()

            elif e0.key == pygame.K_q:
                if self.pointName <= 0:
                    return
                self.pointName -= 1
                # self.render.set_now_name(self.storageName[self.pointName])
            elif e0.key == pygame.K_e:
                if self.pointName + 1 == len(self.storageName):
                    return
                self.pointName += 1
                # self.render.set_now_name(self.storageName[self.pointName])
        elif e0.type == pygame.KEYUP:
            if e0.key == pygame.K_LCTRL:
                self.isCtrlDown = False

    def get_name(self):
        return self.storageName[self.pointName]

    def del_name(self):
        self.storageName.pop(self.pointName)
        if self.pointName == len(self.storageName):
            self.pointName -= 1
        if self.pointName == -1:
            self.storageName.append(None)

    def add_name(self, n0):
        if self.storageName[0] is None:
            self.storageName = []
        self.storageName.append(n0)


class TestWinShow:
    def __init__(self, size, save_path):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.suf = pygame.display.set_mode(size)

        self.render = BgRenderShow(self.suf, save_path)

        self.__winAnchor = self.suf.get_width()//2, self.suf.get_height()//2
        self.isMouseDown = False
        self.isCtrlDown = False

        pygame.event.set_grab(True)

    def update(self):
        self.suf.fill((0, 0, 0))

        self.render.update()

    def event(self, e0):
        if e0.type == pygame.MOUSEMOTION:
            # print(e0.pos)
            x, y = 0, 0
            speed = 1
            if e0.pos[0] == 0:
                x = speed
            elif e0.pos[0] == self.suf.get_width() - 1:
                x = -speed

            if e0.pos[1] == 0:
                y = speed
            elif e0.pos[1] == self.suf.get_height() - 1:
                y = -speed

            if x != 0 or y != 0:
                self.render.set_move_direction((x, y))
            else:
                self.render.set_move_direction()

            # if e0.buttons[2]:
            #     pos = self.render.get_pos()
            #     pos = pos[0] + e0.rel[0], pos[1] + e0.rel[1]
            #     self.render.move(pos=pos)
            # elif e0.buttons[0]:
            #     self.render.event(e0)

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
            # pygame.event.set_grab(False)
            if e0.button == 1:
                self.render.event(e0)

        elif e0.type == pygame.KEYDOWN:
            if e0.key == pygame.K_LCTRL:
                self.isCtrlDown = True
            elif e0.key == pygame.K_q and self.isCtrlDown:
                Core.stop()
            elif e0.key == pygame.K_s and self.isCtrlDown:
                self.render.save()
            elif e0.key == pygame.K_TAB:
                pass

        elif e0.type == pygame.KEYUP:
            if e0.key == pygame.K_LCTRL:
                self.isCtrlDown = False


