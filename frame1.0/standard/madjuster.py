from resource import UnitMaker, resManager, Spirit
from core import Core, Pen

import pygame, os, json
pygame.init()

SOURCE_PATH = r'E:\Date_code\py_data\policyGame\frame1.0\source'
MODE_PATH = r'E:\Date_code\py_data\policyGame\frame1.0\modes'

# check


resManager.load_source(SOURCE_PATH, True)
resManager.load_modes(MODE_PATH, True)


class ModeAdjuster:
    def __init__(self, win_size):
        self.suf = pygame.display.set_mode(win_size)
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}

        self.flip = Flip((win_size[0], 100), self.suf)
        self.action = Action((win_size[0], 100), self.suf)
        self.action.anchor = 0, 100

        self.clock = pygame.time.Clock()
        self.nowMode = None
        self.point_now = 0
        self.point_all = 0

        for i in resManager.m:
            self.point_all += len(i)

        self.gaped = None
        self.actions = []
        self.now_action = 0

        self.bgColor = pygame.color.Color(0, 0, 0)

        self.keyCtrlDown = False

        size = resManager.blockSize
        self.scaleList = [size]
        self.nowScalePoint = 0
        while 1:
            if size[0] < resManager.blockSize[0] // 4 and \
                    size[1] < resManager.blockSize[1] // 4:
                break
            size = int(size[0] / 1.2), int(size[1] / 1.2)
            self.scaleList.insert(0, size)
            self.nowScalePoint += 1
        size = resManager.blockSize
        while 1:
            if size[0] > resManager.blockSize[0] * 4 and \
                    size[1] > resManager.blockSize[1] * 4:
                break
            size = int(size[0] * 1.2), int(size[1] * 1.2)
            self.scaleList.append(size)

        print(self.swap(0))
        # print(resManager.m)

    def update(self):
        self.suf.fill(self.bgColor)
        self.flip.update()
        self.action.update()
        if self.nowMode:
            self.nowMode.update(self.clock.get_time())
        if self.gaped:
            p1 = self.nowMode.get_pos()
            p2 = self.gaped.get_pos()
            size = self.gaped.get_size()
            rect = pygame.rect.Rect(p1[0]+p2[0], p1[1]+p2[1], size[0], size[1])
            pygame.draw.rect(self.suf, (0, 0, 0), rect, 1)

    def event(self, e1):
        if not self.nowMode:
            return
        if e1.type == pygame.MOUSEBUTTONDOWN:
            if self.flip.contains(e1.pos):
                self.flip.event(e1)
                return
            if self.action.contains(e1.pos):
                self.action.event(e1)
        # move
        if e1.type == pygame.MOUSEMOTION:
            if e1.buttons[2]:
                if not self.gaped:
                    pos = self.nowMode.get_pos()
                    pos = pos[0] + e1.rel[0], pos[1] + e1.rel[1]
                    self.nowMode.move(pos=pos)
                else:
                    pos = self.gaped.get_offset_rate()
                    pos = pos[0] + e1.rel[0] // 1, pos[1] + e1.rel[1] // 1
                    self.gaped.set_offset_rate(pos)
                pygame.event.set_grab(True)
            elif e1.buttons[0] and self.gaped:
                pass
                # if not self.gaped:
                #     self.gaped.set_offset_rate(pos=e1.rel)
                #     pygame.event.set_grab(True)
                # else:
                #     pos = self.gaped.get_offset_rate()
                #     pos = pos[0] + e1.rel[0] // 1, pos[1] + e1.rel[1] // 1
                #     self.gaped.set_offset_rate(pos)
        # scale
        elif e1.type == pygame.MOUSEBUTTONDOWN:
            if e1.button == 5:
                if not self.gaped:
                    if self.nowScalePoint + 1 >= len(self.scaleList):
                        return
                    self.nowScalePoint += 1
                    self.nowMode.scale(self.scaleList[self.nowScalePoint])
                else:
                    size = self.gaped.get_offset_size()
                    size = size[0] + 1, size[1] + 1
                    self.gaped.set_offset_size(size)
            elif e1.button == 4:
                if not self.gaped:
                    if self.nowScalePoint - 1 < 0:
                        return
                    self.nowScalePoint -= 1
                    self.nowMode.scale(self.scaleList[self.nowScalePoint])
                else:
                    size = self.gaped.get_offset_size()
                    size = size[0] - 1, size[1] - 1
                    self.gaped.set_offset_size(size)
            elif e1.button == 1:
                self.gaped = self.nowMode.collide_point(e1.pos)

        elif e1.type == pygame.MOUSEBUTTONUP:
            pygame.event.set_grab(False)
            # self.nowMode.event(e1)

        elif e1.type == pygame.KEYDOWN:
            if e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = True
            elif e1.key == pygame.K_s:
                if not self.keyCtrlDown:
                    return
                # self.save()
            elif e1.key == pygame.K_q:
                if not self.keyCtrlDown:
                    return
                Core.overed = True
        elif e1.type == pygame.KEYUP:
            if e1.key == pygame.K_LCTRL:
                self.keyCtrlDown = False

    def swap(self, step) -> str:
        if step + self.point_now < 0:
            self.point_now = 0
        elif step + self.point_now >= self.point_all:
            self.point_now = self.point_all - 1
        if self.point_now == self.point_all:
            self.gaped = None
            return ''

        now = self.point_now
        for i in resManager.m:
            if len(i) <= now:
                now -= len(i)
            else:
                self.nowMode = Spirit(i[now], self.suf)
                self.actions = self.nowMode.get_all_actions()
                self.now_action = 0
                self.swap_action(0)
                self.nowMode.move(200, 200)
                self.nowMode.scale(size=self.scaleList[self.nowScalePoint])
                return i[now].edit_path

        return ''

    def swap_action(self, step) -> str:
        if self.now_action + step >= len(self.actions):
            self.now_action = len(self.actions) - 1
        elif self.now_action + step < 0:
            self.now_action = 0
        act = self.actions[self.now_action]
        self.nowMode.swap(act[1], act[0])
        # if self.gaped:
        #     self.gaped.swap(act[1], act[0])
        return '-'.join(self.actions[self.now_action])

    def swap_layer(self, step) -> int:
        self.nowMode.edited = True
        return self.nowMode.swap_layer(self.gaped, step)

    def set_offset_rate(self, rel):
        size = self.gaped.get_pos()
        size = size[0] + rel[0], size[1] + rel[1]
        size_ = self.nowMode.get_pos()
        rate = size[0] * 100 / size_[0], size[1] * 100 / size_[1]
        self.nowMode.set_offset_rate(rate)
        self.nowMode.edited = True

    def set_offset_size(self, rel):
        size = self.gaped.get_size()
        size = size[0] + rel[0], size[1] + rel[1]
        size_ = self.nowMode.get_size()
        rate = size[0] * 100 / size_[0], size[1] * 100 / size_[1]
        self.nowMode.set_offset_size(rate)
        self.nowMode.edited = True

    @staticmethod
    def save():
        resManager.save_modes(SOURCE_PATH)


class Flip(pygame.surface.Surface):
    def __init__(self, size, pen):
        super(Flip, self).__init__(size)
        self.pen = pen
        self.anchor = 0, 0
        self.bgColor = (0, 0, 0)
        self.legalEvents = {pygame.MOUSEBUTTONDOWN}
        self.step_up = pygame.rect.Rect(0, 0, 30, 20)
        self.step_down = pygame.rect.Rect(0, 30, 30, 20)
        self.stepNu = 1
        self.stepAnchor = 32, 0
        self.to_up = pygame.rect.Rect(60, 0, 30, 20)
        self.to_down = pygame.rect.Rect(60, 30, 30, 20)
        self.track = ''
        self.trackAnchor = 100, 0

    def update(self):
        self.pen.blit(self, self.anchor)
        self.fill(self.bgColor)
        pygame.draw.rect(self, (100, 250, 0), self.step_up)
        pygame.draw.rect(self, (100, 100, 250), self.step_down)
        self.blit(Pen.render(str(self.stepNu)), self.stepAnchor)
        pygame.draw.rect(self, (100, 250, 0), self.to_up)
        pygame.draw.rect(self, (100, 100, 250), self.to_down)
        self.blit(Pen.render(self.track), self.trackAnchor)

    def event(self, e1):
        if e1.button == 0:
            if self.step_up.collidepoint(e1.pos[0], e1.pos[1]):
                self.stepNu = self.stepNu // 5 * 5 + 5
            elif self.step_down.collidepoint(e1.pos[0], e1.pos[1]):
                self.stepNu = self.stepNu - 5
                if self.stepNu <= 0:
                    self.stepNu = 1
            elif self.to_up.collidepoint(e1.pos[0], e1.pos[1]):
                self.track = self.pen.swap(self.stepNu)
            elif self.to_down.collidepoint(e1.pos[0], e1.pos[1]):
                self.track = self.pen.swap(-self.stepNu)
        elif e1.button == 5:
            self.track = self.pen.swap(self.stepNu)
        elif e1.button == 4:
            self.track = self.pen.swap(-self.stepNu)

    def contains(self, pos):
        return self.get_rect().collidepoint(pos[0], pos[1])


class Action(pygame.surface.Surface):
    def __init__(self, size, pen):
        super(Action, self).__init__(size)
        self.pen = pen
        self.anchor = 0, 0
        self.bgColor = (0, 0, 0)

        self.legalEvents = {pygame.MOUSEBUTTONDOWN}
        self.step_up = pygame.rect.Rect(0, 0, 30, 20)
        self.step_down = pygame.rect.Rect(0, 30, 30, 20)
        self.stepNu = ''
        self.stepAnchor = 32, 0

    def update(self):
        self.pen.blit(self, self.anchor)
        self.fill(self.bgColor)
        pygame.draw.rect(self, (100, 250, 0), self.step_up)
        pygame.draw.rect(self, (100, 0, 250), self.step_down)
        self.blit(Pen.render(self.stepNu), self.stepAnchor)

    def event(self, e1):
        if e1.button == 0:
            if self.step_up.collidepoint(e1.pos[0], e1.pos[1]):
                self.stepNu = self.pen.swap_action(-1)
            elif self.step_down.collidepoint(e1.pos[0], e1.pos[1]):
                self.stepNu = self.pen.swap_action(1)

    def contains(self, pos):
        return self.get_rect().collidepoint(pos[0], pos[1])


if __name__ == '__main__':
    print(resManager.m[0][0].__dict__)
    Core.add(ModeAdjuster((800, 600)))
    Core.run()
