#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :resource.py
# @Time      :2021/12/19 10:38
# @Author    :russionbear

import os, configparser, shutil, json, re, copy
import pygame
import random
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict

pygame.mixer.init()


class Music:
    def __init__(self, files, mode=-1):
        self.files = files
        self.nowPoint = 0
        self.mode = mode
        # -2 no order;-1 order; 2 choose

        self.stopped = True
        self.locked = False
        self.music = pygame.mixer.music
        self.th = None

    def start(self):
        if not self.files:
            return
        self.stopped = False
        self.locked = False
        self.music.load(self.files[self.nowPoint])
        self.music.play()
        Thread(target=self.run()).start()

    def run(self):
        while not self.stopped:
            while self.music.get_busy() or self.locked:
                pass
            if self.mode == -1:
                self.nowPoint = (self.nowPoint + 1) % len(self.files)
            elif self.mode == -2:
                self.nowPoint = random.randint(0, len(self.files) - 1)
            else:
                # self.nowPoint = self.mode
                self.mode = -2

            self.music.load(self.files[self.nowPoint])
            self.music.play()
        self.music.stop()

    def play(self, file):
        try:
            self.nowPoint = self.files.index(file)
        except ValueError:
            return
        self.locked = True
        if self.mode == -1:
            self.nowPoint = (self.nowPoint - 1 + len(self.files)) % len(self.files)
        else:
            self.mode = self.nowPoint
        self.music.stop()
        self.locked = False

    def pause(self):
        self.locked = True
        self.music.pause()

    def unpause(self):
        self.locked = False
        self.music.unpause()


"""
为快速查找
必须调用super ，且居于索引值和非索引值中间, 必要属性：action, layer
否则，resManager.find(arg=[...]) 可能会出现错误
# 属性尽量小写
"""


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
        obj = copy.deepcopy(self)
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
        rect = self.__collideRect
        self.__collideRect = None
        obj = copy.deepcopy(self)
        obj.rect = rect.copy()
        self.__collideRect = rect
        return obj

    def to_json(self):
        rlt = {
            "collide_rect": self.__collideRect,
        }
        for k, v in self.__actions.items():
            for k1, v1 in v.items():
                layers = v['layer']
                rate = []
                size = []
                for p in layers:
                    rate.append(v['offsetRate'][p])
                    size.append(v['offsetSize'][p])
                rlt['-'.join(['action', k, k1])] = {
                    "layer": layers,
                    "offsetRate": rate,
                    "offsetSize": size
                }
        return rlt

    # def contains(self, pos):
    #     return


class ModeA(Mode):
    def __init__(self, data):
        it = iter(data)
        self.usage = next(it)
        self.flag = next(it)
        self.name = next(it)

        super(ModeA, self).__init__(it)


class ModeMaker:
    @staticmethod
    def make(data):
        return ModeA(data)


"""unit"""


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
    def __init__(self, obj: Mode, pen=None, top=True):
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

        self.swap(obj.get_first_action()[1], obj.get_first_action()[0])

    def swap(self, name, type_=None):
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
            self.scale(pen=self.__pen)

    def set_offset_rate(self, d0):
        if self.__pen:
            self.__offsetRate = d0
            self.scale(pen=self.__pen)

    def get_offset_rate(self):
        return self.__offsetRate

    def get_offset_size(self):
        return self.__offsetSize

    def scale(self, size=None):
        if self.__offsetSize is not None:
            # self.__pen = pen
            print(self.__offsetSize)

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

    def swap_layer(self, obj, step):
        for k, v in self.__body.items():
            if v != obj:
                continue
            if k in self.__renderOrder:
                id_ = self.__renderOrder.index(k)
                if id_ + step < 0 or id_ + step >= len(self.__renderOrder):
                    return id_
                self.__renderOrder.pop(id_)
                self.__renderOrder.insert(id_ + step, v)
                return id_ + step
        return -1

    def set_pen(self, pen):
        self.__pen = pen

    def copy(self):
        suf = self.__suf
        self.__suf = None
        obj = copy.deepcopy(self)
        obj.__suf = suf
        self.__suf = suf
        obj.__pen = None
        obj.__action = obj.__action.copy()
        return obj

    def contains(self, pos):
        pos = pos[0] - self.__anchor[0], pos[1] - self.__anchor[1]
        return self.__suf.get_rect().collidepoint(pos[0], pos[1])

    def collide_point(self, pos):
        if self.contains(pos):
            print('hrere')
            pos = pos[0] - self.__anchor[0], pos[1] - self.__anchor[1]
            for k in reversed(self.__renderOrder):
                if self.__body[k].contains(pos):
                    return self.__body[k]

    def to_json(self):
        return self.__source.to_json()


class Grid:
    pass


class UnitMaker:
    @staticmethod
    def make(data):
        obj = resManager.get(args=data)
        print(obj, data)
        if obj is None:
            raise OSError
        return Spirit(resManager.get(args=data))


"""mode adjuster"""


class ModeAdjuster:
    pass


"""resource manager"""


class ResManager:
    def __init__(self):
        self.blockSize = 100, 100

        self.musicDrt = None

        self.d = []
        self.index = {}

        self.editPath = {}

        self.m = []
        self.modes = {}

        # self.basicSprite = set()
        # self.layers = {}
        # self.load_source(source_path)

    @staticmethod
    def make_action(root, action, font_path, font_size=20):
        conf = configparser.ConfigParser()
        conf.add_section('action')
        conf.set('action', 'duration', str(2.2))
        conf.set('action', 'merged', '0')
        conf.set('action', 'can_edit', '1')
        conf.set('action', 'mini_color', '1, 2, 3')
        conf.write(open(root + '/guard.ini', 'w', encoding='utf-8'))

        begin_color = []
        end_color = []
        cen_color = []
        for i in range(3):
            begin_color.append(random.randint(0, 255))
            end_color.append(random.randint(0, 255))
            cen_color.append(begin_color[i] - end_color[i])

        for i1, i in enumerate(cen_color):
            cen_color[i1] = i / 10

        for i in range(10):
            now_color = [int(cen_color[j] * i + begin_color[j]) for j in range(3)]
            img = Image.new('RGB', (50, 50), tuple(now_color))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_path, font_size)
            draw.text((0, 0), action, (0, 0, 0), font)
            with open(root + '/' + str(i) + '.jpg', 'wb') as f:
                img.save(f)

    @staticmethod
    def make_test_source(root, actions, font_path, font_size=20):
        for i in actions:
            if os.path.exists(root + '/' + i):
                shutil.rmtree(root + '/' + i)
            os.mkdir(root + '/' + i)
            ResManager.make_action(root + '/' + i, i.split('-')[-1], font_path, font_size)
        conf = configparser.ConfigParser()
        conf.add_section('setting')
        conf.set('setting', 'block_width', str(50))
        conf.set('setting', 'block_height', str(50))
        conf.write(open(root + '/guard.ini', 'w', encoding='utf-8'))

    @staticmethod
    def make_test_source_by_tree(root, tree, font_path, font_size=20):
        rlt = []
        keys = []

        def wash(tree_):
            if isinstance(tree_, list):
                # print(keys, tree_)
                for i_ in tree_:
                    keys.append(i_)
                    rlt.append('-'.join(keys))
                    keys.pop()
                return
            for k_, v_ in tree_.items():
                keys.append(k_)
                wash(v_)
                keys.pop()

        wash(tree)

        ResManager.make_test_source(root, rlt, font_path, font_size)

    def load_music(self, path):
        pass

    def load_source(self, file_path, edit=False):
        if not os.path.exists(file_path):
            return
        if not os.path.isdir(file_path):
            return
        if 'guard.ini' not in os.listdir(file_path):
            return

        conf = configparser.ConfigParser()
        conf.read(file_path + '/guard.ini')
        self.blockSize = conf.getint('setting', 'block_width'), \
                         conf.getint('setting', 'block_height')

        for file in os.listdir(file_path):
            if file == 'guard.ini':
                continue
            conf = configparser.ConfigParser()
            if not os.path.isdir(file_path + '/' + file):
                continue
            conf.read(file_path + '/' + file + '/guard.ini')

            if not conf.getboolean('action', 'can_edit') and edit:
                continue

            track: List[...] = file.split('.')[0].split('-')

            ds = os.listdir(file_path + '/' + file)
            ds.remove('guard.ini')

            # id
            track.append(len(self.d))

            # sound
            for i in ds:
                if i.split('.')[0] == 'sound':
                    track.append(file_path + '/' + file + '/' + i)
                    ds.remove(i)
                    break
            else:
                track.append(None)

            pri_size = self.blockSize

            if conf.has_option('action', 'block_width'):
                self.blockSize = conf.getint('action', 'block_width'), \
                                 conf.getint('action', 'block_height')

            # images
            images = []
            if not conf.getboolean('action', 'merged'):
                ds.sort()
                for i in ds:
                    edit_path = file_path + '/' + file + '/' + i
                    images.append(
                        pygame.transform.scale(
                            pygame.image.load(edit_path),
                            self.blockSize
                        ))
                    if edit:
                        break

            else:
                rows, cols = conf.getint('action', 'rows'), conf.getint('action', 'cols')
                img = Image.open('images.jpg')
                size = cols * self.blockSize[0], rows * self.blockSize[1]
                img.resize(size)
                bw, bh = size[0] / cols, size[1] / rows
                edit_path = file_path + '/' + file + '/__s0plit_image__.jpg'
                for i in range(rows):
                    for j in range(cols):
                        b1, b2 = j * bw, i * bh
                        b3, b4 = b1 + bw, b2 + bh

                        img.crop((b1, b2, b3, b4)).save(edit_path)

                        images.append(
                            pygame.transform.scale(
                                pygame.image.load(edit_path),
                                self.blockSize
                            ))
                        if edit:
                            break
                    if edit:
                        break

                if os.path.exists(edit_path) and not edit:
                    os.remove(edit_path)

            self.blockSize = pri_size

            track.append(images)

            # gap
            track.append(conf.getfloat('action', 'duration') / len(images))
            # print(track[-1], len(images))

            obj = SourceMaker.make(track)

            if edit:
                self.editPath[obj] = edit_path

            self.d.append(obj)

            tmp_d = self.index
            keys = obj.get_index()[:-1]

            for i in keys:
                if i not in tmp_d:
                    tmp_d[i] = {}
                tmp_d = tmp_d[i]
            tmp_d[track[-5]] = obj

        # print('loaded', self.d, '\n', self.index)

        # if conf.has_option('action', 'mini_color'):
        #     c0 = conf.get('action', 'mini_color')
        #     c0 = c0.split(',')
        #     for i1, i in enumerate(c0):
        #         c0[i1] = int(i)
        #     obj.mini_color = tuple(c0[:3])

    def load_modes(self, file_path, edit=False):
        if not self.d or not os.path.exists(file_path):
            return
        modes1 = {}
        modes2 = []
        # spirits = []
        # it = 1
        it = True
        for i in os.listdir(file_path):
            ds = os.listdir(file_path + '/' + i)
            tmp_m = {}
            tmp1_m = []
            for j in ds:
                tracks: List[...] = j.split('.')[0].split('-')
                with open(file_path + '/' + i + '/' + j, 'r') as f:
                    tmp_data = json.load(f)
                body = {}
                for k, v in tmp_data['name'].items():
                    body[k] = Shard(self.find(args=v.split('-')))
                    # print(body[k])
                for k, v in tmp_data['e-name'].items():
                    tmp_chip = modes1
                    for l in v:
                        tmp_chip = tmp_chip[l]
                    body[k] = Spirit(tmp_chip)
                    body[k] = tmp_chip

                del tmp_data['name']
                del tmp_data['e-name']
                tracks.append(body)
                for k in ['first_action', 'collide_rect', 'mini_color', 'interface']:
                    tracks.append(tmp_data[k])
                    del tmp_data[k]
                actions = {}
                for k, v in tmp_data.items():
                    if 'action-' in k:
                        tmp_k = k.split('-')[1:]
                        if tmp_k[0] not in actions:
                            actions[tmp_k[0]] = {tmp_k[1]: {}}
                        elif tmp_k[1] not in actions[tmp_k[0]]:
                            actions[tmp_k[0]][tmp_k[1]] = {}
                        if 'to' in v:
                            actions[tmp_k[0]][tmp_k[1]]['to'] = v['to']
                        if 'layer' not in v:
                            continue
                        offset_rate = {}
                        offset_size = {}
                        for l1, l in enumerate(v['layer']):
                            offset_rate[l] = v['offset_rate'][l1]
                            offset_size[l] = v['offset_size'][l1]
                        actions[tmp_k[0]][tmp_k[1]]['offset_rate'] = offset_rate
                        actions[tmp_k[0]][tmp_k[1]]['offset_size'] = offset_size
                        actions[tmp_k[0]][tmp_k[1]]['layer'] = v['layer']

                tracks.append(actions)

                if it:
                    obj = ModeMaker.make(tracks)
                else:
                    obj = UnitMaker.make(tracks)

                if edit:
                    obj.edit_path = i + '/' + j
                    obj.edited = False

                tmp_k1 = tmp_m
                for k in tracks[:-7]:
                    if k not in tmp_k1:
                        tmp_k1[k] = {}
                    tmp_k1 = tmp_k1[k]
                tmp_k1[tracks[-7]] = obj

                tmp1_m.append(obj)

            pass
            it = False
            modes1[i] = tmp_m
            modes2.append(tmp1_m)
            # spirits.append()
            # it += 1
        self.m = modes2
        self.modes = modes1

    def save_modes(self, path):
        for i in self.m:
            for j in i:
                if not j.edited:
                    continue
                with open(path + '/' + j.edit_path, 'r') as f:
                    tmp_data = json.load(f)
                j.edited = False
                tmp_d = j.to_json()
                for k, v in tmp_d.items():
                    tmp_data[k] = v
                with open(path + '/' + j.edit_path, 'w') as f:
                    json.dump(tmp_data, f)

    # def load_source(self, filepath: str, edit=False):
    #     filepath = filepath.replace('\\', '/')
    #
    #     q = [filepath+'/'+i for i in os.listdir(filepath)]
    #     ks = ['usage']
    #     vs = []
    #     while q:
    #         d0 = q.pop()
    #
    #         if d0 == 'guard.ini':
    #             continue
    #         # vs.append(os.path.split(d0)[1])
    #         if d0 is None:
    #             ks.pop()
    #             vs.pop()
    #             continue
    #
    #         if not os.path.isdir(d0):
    #             # print(d0, 'path error')
    #             continue
    #
    #         ds = os.listdir(d0)
    #         if not ds:
    #             continue
    #
    #         if 'guard.ini' not in ds:
    #             print('does not has a guard')
    #             raise OSError
    #
    #         conf = configparser.ConfigParser()
    #         conf.read(d0+'/guard.ini')
    #         sections = conf.sections()
    #         # print(sections, d0)
    #         if 'none' in sections:
    #             continue
    #         elif 'pass' in sections:
    #             for i in ds:
    #                 if i == 'guard.ini':
    #                     continue
    #                 q.append(d0+'/'+i)
    #         elif 'key' in sections:
    #             if not conf.getboolean('key', 'canEdit') and edit:
    #                 continue
    #             q.append(None)
    #             vs.append(os.path.split(d0)[1])
    #             ks.append(conf.get('key', 'keyName'))
    #             for i in ds:
    #                 if i == 'guard.ini':
    #                     continue
    #                 q.append(d0+'/'+i)
    #
    #             if conf.has_option('key', 'isBasic') and edit:
    #                 if conf.get('key', 'isBasic') == 'basic':
    #                     self.basicSprite.add(ks[-1])
    #                     # self.basicSprite.append(vs.copy())
    #             # if not conf.getboolean('key', 'canEdit'):
    #             #     self.cantEdit.append(vs.copy())
    #
    #         elif 'action' in sections:
    #             if not conf.getboolean('action', 'canEdit') and edit:
    #                 continue
    #             tmp_k = {ks[-1]: os.path.split(d0)[1]}
    #             ds.remove('guard.ini')
    #
    #             # sound
    #             for i in ds:
    #                 if i.split('.')[0] == 'sound':
    #                     tmp_k['sound'] = d0 + '/' + i
    #                     ds.remove(i)
    #                     break
    #
    #             # images
    #             tmp_k['images'] = []
    #             if not conf.getboolean('action', 'merged'):
    #                 for i in ds:
    #                     edit_path = d0 + '/' + i
    #                     tmp_k['images'].append(
    #                         pygame.transform.scale(
    #                             pygame.image.load(edit_path),
    #                             self.blockSize
    #                         ))
    #
    #             else:
    #                 rows, cols = conf.getint('action', 'rows'), conf.getint('action', 'cols')
    #                 img = Image.open('images.jpg')
    #                 size = cols * self.blockSize[0], rows * self.blockSize[1]
    #                 img.resize(size)
    #                 bw, bh = size[0] / cols, size[1] / rows
    #                 tmp_path = d0+'/__s0plit_image__.jpg'
    #                 for i in range(rows):
    #                     for j in range(cols):
    #                         b1, b2 = j * bw, i * bh
    #                         b3, b4 = b1 + bw, b2 + bh
    #
    #                         img.crop((b1, b2, b3, b4)).save(tmp_path)
    #
    #                         tmp_k['images'].append(
    #                             pygame.transform.scale(
    #                                 pygame.image.load(tmp_path),
    #                                 self.blockSize
    #                             ))
    #                 if os.path.exists(tmp_path) and not edit:
    #                     os.remove(tmp_path)
    #                 edit_path = tmp_path
    #
    #             tmp_d = self.index
    #             for i1, i in enumerate(vs):
    #                 tmp_k[ks[i1]] = i
    #                 if i not in tmp_d:
    #                     tmp_d[i] = {}
    #                 tmp_d = tmp_d[i]
    #             tmp_d[os.path.split(d0)[1]] = tmp_k
    #             tmp_k['id'] = len(self.d)
    #             tmp_k['gap'] = conf.getfloat('action', 'duration') / len(tmp_k['images'])
    #             if edit:
    #                 tmp_k['filepath'] = edit_path
    #             self.d.append(tmp_k)
    #
    #         sections.clear()
    #
    #     if edit:
    #         for i in self.d:
    #             for j in self.basicSprite:
    #                 if j in i:
    #                     i['isBasic'] = 'basic'
    #                     break
    #             else:
    #                 i['isBasic'] = 'not'
    #
    # def make_test_source(self, dr: dict, filepath, font_path):
    #     if os.path.exists(filepath):
    #         if os.path.isdir(filepath):
    #             shutil.rmtree(filepath)
    #         else:
    #             os.remove(filepath)
    #     os.mkdir(filepath)
    #
    #     q = list(dr.keys())
    #     ks = ['usage']
    #     vs = []
    #     while q:
    #         d0 = q.pop()
    #
    #         if d0 == '__guard':
    #             continue
    #
    #         if d0 is None:
    #             ks.pop()
    #             vs.pop()
    #             continue
    #
    #         tmp_dr = dr
    #         for i in vs:
    #             tmp_dr = tmp_dr[i]
    #
    #         tmp_dr = tmp_dr[d0]
    #         tmp_path = filepath + '/' + '/'.join(vs)
    #         if tmp_path[0] == '/':
    #             tmp_path += d0
    #         else:
    #             tmp_path += '/' + d0
    #
    #         if 'none' in tmp_dr['__guard']:
    #             os.mkdir(tmp_path)
    #             conf = configparser.ConfigParser()
    #             conf.add_section('none')
    #             conf.write(open(tmp_path+'/guard.ini', 'w', encoding='utf-8'))
    #             continue
    #
    #         elif 'key' in tmp_dr['__guard']:
    #             os.mkdir(tmp_path)
    #             conf = configparser.ConfigParser()
    #             conf.add_section('key')
    #             conf.set('key', 'keyName', tmp_dr['__guard']['key']['keyName'])
    #             conf.set('key', 'canEdit', '1')
    #             if tmp_dr['__guard']['key']['isBasic'] == 'basic':
    #                 conf.set('key', 'isBasic', 'basic')
    #             conf.write(open(tmp_path+'/guard.ini', 'w', encoding='utf-8'))
    #
    #             q.append(None)
    #             vs.append(d0)
    #             ks.append(tmp_dr['__guard']['key']['keyName'])
    #             q.extend(list(tmp_dr.keys()))
    #
    #         elif 'action' in tmp_dr['__guard']:
    #             action = tmp_dr['__guard']['action']
    #             os.mkdir(tmp_path)
    #             conf = configparser.ConfigParser()
    #             conf.add_section('action')
    #             conf.set('action', 'duration', str(action['duration']))
    #             conf.set('action', 'merged', '0')
    #             conf.set('action', 'canEdit', '1')
    #             conf.write(open(tmp_path+'/guard.ini', 'w', encoding='utf-8'))
    #
    #             begin_color = action['beginColor']
    #             cen_color = [action['endColor'][i]-begin_color[i] for i in range(3)]
    #             for i1, i in enumerate(cen_color):
    #                 cen_color[i1] = i / action['amount']
    #             for i in range(action['amount']):
    #                 now_color = [int(cen_color[j] * i + begin_color[j]) for j in range(3)]
    #                 img = Image.new('RGB', self.blockSize, tuple(now_color))
    #                 draw = ImageDraw.Draw(img)
    #                 font = ImageFont.truetype(font_path, action['fontSize'])
    #                 draw.text((0, 0), d0, action['fontColor'], font)
    #                 with open(tmp_path+'/'+str(i)+'.jpg', 'wb') as f:
    #                     img.save(f)

    def find(self, kwargs=None, args=None, cursor=None):
        """
        默认浅复制
        :param kwargs:
        :param args:
        :param cursor:
        :return:
        """
        if kwargs is not None:
            return self.__find_by_ergodic(**kwargs)
        elif args is not None:
            # print("args", args)
            obj = self.__find_by_index(*args)
            if obj is None:
                print('None', args)
                raise OSError
            # print(obj, self.index)
            return obj
        else:
            if cursor < 0 or cursor >= len(self.d):
                return None
            return self.d[cursor]

    def __find_by_index(self, *args):
        rlt = self.index
        for i in args:
            if i not in rlt:
                return None
            rlt = rlt[i]
        else:
            return rlt

    def __find_by_ergodic(self, **kwargs):
        for i in self.d:
            for k, v in kwargs.items():
                if k in i.__dict__:
                    if i.__dict__[k] != v:
                        break
                else:
                    break
            else:
                return i
        else:
            return None

    def find_all(self, kwargs):
        rlt = []
        for i in self.d:
            for k, v in kwargs.items():
                if i.__dict__[k] != v:
                    break
            else:
                rlt.append(i)
        return rlt

    def get_all(self, kwargs):
        rlt = []
        for i in self.m:
            for k, v in kwargs.items():
                if i.__dict__[k] != v:
                    break
            else:
                rlt.append(i)
        return rlt

    def get(self, kwargs=None, args=None, cursor=None):
        """

        :param kwargs:
        :param args:
        :param cursor:
        :return: Mode
        """
        if kwargs is not None:
            return self.__get_by_ergodic(**kwargs)
        elif args is not None:
            return self.__get_by_index(*args)
        else:
            if cursor < 0 or cursor >= len(self.m):
                return None
            return self.m[cursor]

    def __get_by_index(self, *args):
        rlt = self.modes
        for i in args:
            if i not in rlt:
                return None
            rlt = rlt[i]
        # else:
        return rlt.copy()

    def __get_by_ergodic(self, **kwargs):
        for i in self.m:
            for k, v in kwargs.items():
                if k in i.__dict__:
                    if i.__dict__[k] != v:
                        break
                # else:
                #     break
            else:
                return i
                # return i.copy()
        return None

    # def get_source(self, action, root):
    #     rlt = self.index
    #     for i in root:
    #         rlt = rlt[i]
    #     obj = Source(self, action, rlt[action]['images'], root)
    #     return obj


resManager = ResManager()

# resManager.get().


if __name__ == '__main__':
    where = 'load_modes'
    if where == 'make_source':
        dd2 = r'E:\Date_code\py_data\policyGame\frame1.0\source'
        # dd3 = ['geo-tree-stand', 'unit-red-man-left',
        #        'unit-red-man-right', 'unit-red-man-up',
        #        'unit-red-man-low']
        dd3 = {
            "geo": {
                "tree": ['stand']
            },
            "unit": {
                "flag": {"footmen": ['stand', 'move', 'fly']}
            },
            "tag": {
                "number": [str(i) for i in range(1, 11)]
            }
        }
        ResManager.make_test_source_by_tree(r'E:\Date_code\py_data\policyGame\frame1.0\source',
                                            dd3,
                                            r'E:\Date_code\py_data\yazha_1\msyh.ttc')

    elif where == 'test':
        r1 = ResManager()
        r1.load_source(r'E:\Date_code\py_data\policyGame\frame1.0\source', True)
        r1

    elif where == 'load_modes':
        r1 = ResManager()
        r1.load_source(r'E:\Date_code\py_data\policyGame\frame1.0\source', True)
        print(r1.d, '\n', r1.index)
        r1.load_modes(r'E:\Date_code\py_data\policyGame\frame1.0\modes')
        print(r1.m)
        for i in r1.m[0]:
            print(i.__dict__)
