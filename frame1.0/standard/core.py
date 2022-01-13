# coding: utf-8
import pygame
from queue import Queue
from threading import Thread
pygame.init()


class _Core:
    def __init__(self):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                            pygame.MOUSEBUTTONUP,
                            pygame.MOUSEMOTION,
                            pygame.KEYDOWN,
                            pygame.KEYUP}
        self.listener = []
        self.overed = False
        self.th = None

    def run(self):
        self.overed = False
        while not self.overed:
            for e0 in pygame.event.get():
                if e0.type == pygame.QUIT:
                    pygame.quit()
                    return
                # if e0.type not in self.legalEvents:
                #     continue
                # for i in self.listener:
                #     if e0.type in i.legalEvents:
                #         i.event(e0)
                if self.listener:
                    if e0.type in self.listener[-1].legalEvents:
                        self.listener[-1].event(e0)

            # for i in self.listener:
            #     i.update()
            self.listener[-1].update()

            pygame.display.update()

    def start(self):
        self.overed = True
        # self.run()
        # if not self.th:
        #     self.th = Thread(target=self.run).start()
        # elif not self.th.isAlive():
        #     self.th = Thread(target=self.run).start()

    def stop(self):
        self.overed = True

    # def show(self):
    #     if not self.th:
    #         self.start()
    #     elif not self.th.isAlive():
    #         self.start()
    #
    def hide(self):
        self.stop()
        pygame.display.iconify()
        # pygame.display

    def add(self, obj):
        if obj not in self.listener:
            self.listener.append(obj)

    def remove(self, obj):
        self.listener.remove(obj)

    def push(self, obj):
        self.listener.append(obj)

    def pop(self):
        self.listener.pop()

    def clear(self):
        self.listener.clear()

    def has(self, obj):
        return obj in self.listener


class _Pen:
    Pens = {}

    def __init__(self):
        self.font = "SimHei"
        self.size = 30
        self.pen = pygame.font.SysFont(self.font, self.size)
        self.fg = (0, 0, 255)
        self.bg = None
        # self.__pens = {}

    @classmethod
    def make_pen(cls, size, font):
        k0 = (size, hash(font))
        if k0 in cls.Pens:
            return cls.Pens[k0]
        obj = cls()
        obj.font = font
        obj.size = size
        obj.pen = pygame.font.SysFont(font, size)
        # obj =
        cls.Pens[k0] = obj
        return obj

    @classmethod
    def del_pen(cls, size, font):
        del cls.Pens[(size, hash(font))]

    def set(self, size=None, font=None):
        if size:
            self.size = size
        if font:
            self.font = font
        self.pen = pygame.font.SysFont(self.font, self.size)

    def render(self, text, fg=None, bg=None):
        if fg is None:
            fg = self.fg
        if bg is None:
            bg = self.bg
        return self.pen.render(text, True, fg, bg)

    def get_font_size(self):
        return self.size

    @staticmethod
    def to_std_size(ustring):
        """半角转全角"""
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 32:
                inside_code = 12288
            elif 32 <= inside_code <= 126:
                inside_code += 65248
            rstring += chr(inside_code)
        return rstring

    def get_width(self, s0):
        width = 0
        for i in s0:
            c_ord = ord(i)
            if 32 <= c_ord <= 126:
                width += 1
            else:
                width += 2
        return width * self.size // 2

    def cut_by_size(self, s0, s, rvs=False):
        width = 0
        if rvs:
            s1 = reversed(s0)
        else:
            s1 = s0

        for i1, i in enumerate(s1):
            c_ord = ord(i)
            if 32 <= c_ord <= 126:
                width += self.size / 2
                if width > s:
                    if rvs:
                        return s0[-i1:]
                    return s0[:i1-1]
            else:
                width += self.size
                if width > s:
                    if rvs:
                        return s0[-i1:]
                    return s0[:i1-1]

        # if rvs:
        #     return list(s1)
        return s0

    # def get_height(self, s0):
    #     for i in s0:
    #         c_ord = ord(i)
    #         if c_ord == 12288 or 65280 <= c_ord <=65374:
    #             return self.size
    #     return self.size // 2


class _Consigner:
    def __init__(self):
        self.begins = {}
        self.signs = Queue(128)
        self.overed = False

    def update(self):
        while not self.signs.empty():
            pass
    # def run(self):
    #     while not self.overed:
    #         cur = self.signs.get()
    #         self.begins[cur].slots(cur[1])

    def register(self, begin, end, type_):
        cur = (begin, type_)
        self.begins[cur] = end
        # if end not in self.ends:
        #     self.ends[end] = set()
        # self.ends[end].add(begin)

    def send(self, obj, type_):
        while self.signs.full():
            pass
        cur = (obj, type_)
        self.signs.put(cur)

    def remove(self, obj, type_=None):
        if not type_:
            should_d = []
            for k, v in self.begins.items():
                if v == obj or k[0] == obj:
                    should_d.append(k)
            for k in should_d:
                del self.begins[k]

        cur = (obj, type_)
        if cur in self.begins:
            del self.begins[cur]

    @staticmethod
    def post(obj, type_, kwargs):
        obj.slots(type_, kwargs)


class _Motor:
    move = 1
    scale = 2

    def __init__(self):
        self.__move = set()

    def add(self, obj):
        self.__move.add(obj)

    def remove(self, obj):
        self.__move.remove(obj)

    def update(self):
        should_d = set()
        for i in self.__move:
            if i.auto_move():
                should_d.add(i)
        for i in should_d:
            self.__move.remove(i)


Core = _Core()

Pen = _Pen()

Consigner = _Consigner()

Motor = _Motor()


# pygame.image.load().
