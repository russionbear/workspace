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
        while not self.overed:
            for e0 in pygame.event.get():
                if e0.type == pygame.QUIT:
                    pygame.quit()
                    return
                if e0.type not in self.legalEvents:
                    continue
                for i in self.listener:
                    if e0.type in i.legalEvents:
                        i.event(e0)

            for i in self.listener:
                i.update()

            pygame.display.update()

    def start(self):
        if not self.th:
            self.th = Thread(target=self.run).start()
        elif not self.th.isAlive():
            self.th = Thread(target=self.run).start()

    def stop(self):
        self.overed = True

    # def show(self):
    #     if not self.th:
    #         self.start()
    #     elif not self.th.isAlive():
    #         self.start()
    #
    # def hide(self):
    #     pygame.display.iconify()
    #     self.stop()

    def add(self, obj):
        if obj not in self.listener:
            self.listener.append(obj)

    def remove(self, obj):
        self.listener.remove(obj)

    def has(self, obj):
        return obj in self.listener


class _Pen:
    def __init__(self):
        self.font = "arial"
        self.size = 30
        self.pen = pygame.font.SysFont(self.font, self.size)

    def set(self, size=None, font=None):
        if size:
            self.size = size
        if font:
            self.font = font
        self.pen = pygame.font.SysFont(self.font, self.size)

    def render(self, text, fg=pygame.color.Color(0, 0, 255), bg=None):
        return self.pen.render(text, True, fg, bg)


class _Consigner:
    def __init__(self):
        self.begins = {}
        self.signs = Queue(128)
        self.overed = False

    def run(self):
        while not self.overed:
            cur = self.signs.get()
            self.begins[cur].slots(cur[1])

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
        self.__data = []

    # def


Core = _Core()

Pen = _Pen()

Consigner = _Consigner()

Motor = _Motor()


# pygame.image.load().
