import pygame
import sys
from ..core import Pen, Core
import pickle, os


class MainView:
    def __init__(self, save_path):
        self.savePath = save_path
        self.suf = pygame.display.set_mode((800, 800))
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}
        self.img = pygame.image.load(save_path+'/map.jpg')
        self.priImg = self.img.copy()
        self.anchor = 0, 0
        self.bgColor = pygame.color.Color(0, 0, 0)
        self.showTool = False
        self.tool = Tool(self.suf.get_size())

        size = self.img.get_size()
        self.scaleList = [size]
        self.nowScalePoint = 0
        while 1:
            if size[0] < self.suf.get_width() // 2 and \
                    size[1] < self.suf.get_height() // 2:
                break
            size = int(size[0] / 1.2), int(size[1] / 1.2)
            self.scaleList.insert(0, size)
            self.nowScalePoint += 1
        size = self.img.get_size()
        while 1:
            if size[0] > self.suf.get_width() * 4 and \
                    size[1] > self.suf.get_height() * 4:
                break
            size = int(size[0] * 1.2), int(size[1] * 1.2)
            self.scaleList.append(size)

        self.cities = []
        self.roads = []
        self.logs = []
        self.keyCtrlDown = False

        if os.path.exists(save_path+'/points'):
            with open(save_path+'/points', 'rb') as f:
                tmp = pickle.load(f)
            for i in tmp['cities']:
                self.cities.append((i[0], i[1], self.nowScalePoint))
            for i in tmp['roads']:
                self.cities.append((i[0], i[1], self.nowScalePoint))

    def update(self):
        self.suf.fill(self.bgColor)
        self.suf.blit(self.img, self.anchor)
        if self.showTool:
            self.tool.update()
        for i in self.cities:
            n = self.scaleList[self.nowScalePoint][0] / self.scaleList[i[2]][0]
            pos = i[0] * n + self.anchor[0], i[1] * n + self.anchor[1]
            pygame.draw.circle(self.suf, (255, 0, 0), pos, 5, 5)
        for i in self.roads:
            n = self.scaleList[self.nowScalePoint][0] / self.scaleList[i[2]][0]
            pos = i[0] * n + self.anchor[0], i[1] * n + self.anchor[1]
            pygame.draw.circle(self.suf, (0, 0, 255), pos, 5, 5)

    def event(self, e1):
        if e1.type == pygame.MOUSEMOTION:
            if self.showTool:
                return
            if e1.buttons[2]:
                self.move(pos=e1.rel)
                pygame.event.set_grab(True)
            elif e1.buttons[0]:
                self.handle(e1)
        elif e1.type == pygame.MOUSEBUTTONDOWN:
            if self.showTool:
                self.tool.event(e1)
            elif e1.button == 1:
                self.logs.append(0)
                self.handle(e1)
            else:
                if e1.button == 5:
                    self.scale(-1)
                elif e1.button == 4:
                    self.scale(1)
        elif e1.type == pygame.MOUSEBUTTONUP:
            pygame.event.set_grab(False)
        elif e1.type == pygame.KEYDOWN:
            if e1.key == pygame.K_TAB:
                self.showTool = not self.showTool
            elif e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = True
            elif e1.key == pygame.K_z:
                if self.logs and self.keyCtrlDown and not self.showTool:
                    while 1:
                        tmp = self.logs.pop()
                        if tmp == 0:
                            break
                        if tmp == self.tool.City:
                            self.cities.pop()
                        else:
                            self.roads.pop()
            elif e1.key == pygame.K_s:
                if self.showTool or not self.keyCtrlDown:
                    return
                self.save()
            elif e1.key == pygame.K_q:
                if self.showTool or not self.keyCtrlDown:
                    return
                Core.overed = True
        elif e1.type == pygame.KEYUP:
            if e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = False

    def move(self, y=0, x=0, pos=None):
        if pos:
            y, x = pos
        self.anchor = self.anchor[0] + y, self.anchor[1] + x

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

        self.anchor = self.anchor[0] + (self.img.get_width() - size[0]) / 2, \
                      self.anchor[1] + (self.img.get_height() - size[1]) / 2

        self.img = pygame.transform.scale(self.priImg, size)

    def handle(self, e1):
        if not self.tool.nowP:
            return
        rect = self.img.get_rect().move(self.anchor[0], self.anchor[1])
        if not rect.collidepoint(e1.pos[0], e1.pos[1]):
            return
        if self.tool.nowP == self.tool.City:
            for i in self.cities:
                if ((e1.pos[0] - i[0] + self.anchor[0]) ** 2 + (e1.pos[1] - i[1] + self.anchor[1]) ** 2) ** 0.5 < 50:
                    break
            else:
                self.cities.append((e1.pos[0] - self.anchor[0],
                                    e1.pos[1] - self.anchor[1],
                                    self.nowScalePoint))
                self.logs.append(self.tool.City)
        elif self.tool.nowP == self.tool.Road:
            for i in self.roads:
                if ((e1.pos[0] - i[0] + self.anchor[0]) ** 2 + (e1.pos[1] - i[1] + self.anchor[1]) ** 2) ** 0.5 < 10:
                    break
            else:
                self.roads.append((e1.pos[0] - self.anchor[0],
                                   e1.pos[1] - self.anchor[1],
                                   self.nowScalePoint))
                self.logs.append(self.tool.Road)

    def save(self):
        pygame.image.save(self.img, self.savePath+'\\'+'map.jpg')
        tmp = {'cities': self.cities, 'roads': self.roads}
        with open(self.savePath+'/points', 'wb') as f:
            f.write(pickle.dumps(tmp))


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
