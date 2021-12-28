# from . resource import ResManager


# class Source:
#     def __init__(self, boss: ResManager, action, prim_images, root):
#         self.boss = boss
#         self.root = root
#         self.action = action
#
#         self.__priImages = prim_images
#         self.images = prim_images[:]
#         self.nowPoint = 0
#         self.nowImage = self.images[0]
#
#         self.sound = None
#
#         self.gap = 0
#         self.nowTime = 0.0
#
#     def scale(self, size):
#         if self.nowImage.get_width() > size[0]:
#             for i1, i in enumerate(self.images):
#                 self.images[i1] = pygame.transform.scale(i, size)
#         else:
#             for i1, i in enumerate(self.__priImages):
#                 self.images[i1] = pygame.transform.scale(i, size)
#
#     def get(self):
#         return self.nowImage
#
#     def update(self, t0):
#         self.nowTime += t0
#         if self.nowTime > self.gap:
#             self.nowTime = 0.0
#             self.nowPoint = (self.nowPoint + 1) % len(self.images)
#             self.nowImage = self.images[self.nowPoint]
#
#     def swap(self, name):
#         size = self.nowImage.get_size()
#         self.root.append(name)
#         obj = self.boss.find(True, self.root)
#         self.__priImages = obj['images']
#         self.images = self.__priImages.copy()
#         self.scale(size)
#
#         self.nowImage = self.images[0]
#         self.nowPoint = 0
#         self.gap = obj['gap']
#
#         self.root.pop()
#         self.action = name
#
#         if 'sound' in obj:
#             self.sound = obj['sound']
#
#     def play(self):
#         if self.sound is not None:
#             pygame.mixer.Sound(self.sound).play(1)
import copy


class TrackBasic:
    def __init__(self, data):
        it = iter(data)
        self.usage: str = it.__next__()
        self.name: str = it.__next__()
        self.action: str = it.__next__()
        self.sound: str = it.__next__()
        self.images = it.__next__()
        self.gap: float = it.__next__()
        self.layer = 0
        self.id = 0


class TrackUnit:
    def __init__(self, data):
        it = iter(data)
        self.usage: str = it.__next__()
        self.flag: str = it.__next__()
        self.name: str = it.__next__()
        self.action: str = it.__next__()
        self.sound: str = it.__next__()
        self.images: list = it.__next__()
        self.gap: float = it.__next__()
        self.layer = 1


class TrackMaker:
    @staticmethod
    def make(l0):
        """

        :param l0:
        :return: TrackBasic, TrackUnit
        """
        if l0[0] == 'geo':
            return TrackBasic(l0)
        elif l0[0] == 'unit':
            return TrackUnit(l0)


class Win:
    def __init__(self, p0):
        self.__name = p0

    def print(self):
        print(self.__name)

    def copy(self):
        obj = copy.deepcopy(self)
        obj.__name = '123'
        return obj

    @staticmethod
    def swap():
        return Win(123)


class Yun:
    def __init__(self, l0):
        self.name = l0

    def jj(self, obj):
        # obj =
        pass


if __name__ == '__main__':
    l0 = []
    l0.insert(0, 1)