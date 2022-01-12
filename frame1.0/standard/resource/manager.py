#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :manager.py
# @Time      :2022/1/2 15:40
# @Author    :russionbear

# from __future__ import print_function
# from .unit import Shard, Spirit, UnitMaker
# from .source import SourceMaker
# from .mode import ModeMaker

import configparser
import random
import json
import os
import shutil
from typing import List
import pygame
from PIL import Image, ImageDraw, ImageFont

pygame.display.init()

"""resource manager"""


class ResMng:
    def __init__(self):
        self.blockSize = 100, 100

        self.musicDrt = None
        self.modeDrt = None
        self.sourceDrt = None

        self.d = []
        self.index = {}

        self.editPath = {}

        self.m = []
        self.modes = {}

        self.menuImages = {}

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
            ResMng.make_action(root + '/' + i, i.split('-')[-1], font_path, font_size)
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

        ResMng.make_test_source(root, rlt, font_path, font_size)

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

        self.sourceDrt = file_path
        # print('loaded', self.d, '\n', self.index)

        # if conf.has_option('action', 'mini_color'):
        #     c0 = conf.get('action', 'mini_color')
        #     c0 = c0.split(',')
        #     for i1, i in enumerate(c0):
        #         c0[i1] = int(i)
        #     obj.mini_color = tuple(c0[:3])

    def load_modes(self, file_path, mode=0):
        """
        mode: 0: play, 1:source edit, 2: map edit
        """
        if not self.d or not os.path.exists(file_path):
            return
        modes1 = {}
        modes2 = []
        # spirits = []
        # it = 1
        it = True
        for i in os.listdir(file_path):
            if os.path.isfile(file_path + '/' + i):
                continue
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

                if mode == 1:
                    obj.edit_path = i + '/' + j
                    obj.edited = False
                elif mode == 2:
                    obj.edit_path = j.split('.')[0]

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

        if mode == 2 or mode == 0:
            for i in modes2:
                for j in i:
                    if j.is_interface():
                        self.m.append(j)
            for k, v in modes1.items():
                self.modes.update(v)
        elif mode == 1:
            self.m = modes2
            self.modes = modes1

        self.modeDrt = file_path

    def load_menu_source(self, path):
        for i in os.listdir(path):
            names = i.split('.')[0].split('_')
            tmp = self.menuImages
            for i in names[:-1]:
                if i not in tmp:
                    tmp[i] = {}
                tmp = tmp[i]
            # name = i.split('.')[0]
            tmp[names[-1]] = pygame.image.load(path + '/' + i)
            # self.menuImages[name] = pygame.image.load(path + '/' + i)

    def save_modes(self, path, spirit, **kwargs):
        with open(path, 'r') as f:
            tmp_d = json.load(f)
        tmp_dd = spirit.to_json()
        for k, v in tmp_dd.items():
            tmp_d[k] = v
        with open(path, 'w') as f:
            json.dump(tmp_d, f)
        pass
        # for i in self.m:
        #     for j in i:
        #         if not j.edited:
        #             continue
        #         with open(path + '/' + j.edit_path, 'r') as f:
        #             tmp_data = json.load(f)
        #         j.edited = False
        #         tmp_d = j.to_json()
        #         for k, v in tmp_d.items():
        #             tmp_data[k] = v
        #         with open(path + '/' + j.edit_path, 'w') as f:
        #             json.dump(tmp_data, f)

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
            return rlt.copy()

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
        return rlt

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

    def get_menu_image(self, k0):
        tmp = self.menuImages
        for i in k0:
            tmp = tmp[i]
        return tmp
        # return self.menuImages[name]


# class ResMngAdj(ResMng):
#     def save_modes(self, path, spirit, **kwargs):
#         with open(path, 'r') as f:
#             tmp_d = json.load(f)
#         tmp_dd = spirit.to_json()
#         for k, v in tmp_dd.items():
#             tmp_d[k] = v
#         with open(path, 'w') as f:
#             json.dump(tmp_d, f)
#         pass
#         # for i in self.m:
#         #     for j in i:
#         #         if not j.edited:
#         #             continue
#         #         with open(path + '/' + j.edit_path, 'r') as f:
#         #             tmp_data = json.load(f)
#         #         j.edited = False
#         #         tmp_d = j.to_json()
#         #         for k, v in tmp_d.items():
#         #             tmp_data[k] = v
#         #         with open(path + '/' + j.edit_path, 'w') as f:
#         #             json.dump(tmp_data, f)
#
#     def __get_by_index(self, *args):
#         rlt = self.modes
#         for i in args:
#             if i not in rlt:
#                 return None
#             rlt = rlt[i]
#         # else:
#         return rlt
#
#     def __get_by_ergodic(self, **kwargs):
#         for i in self.m:
#             for k, v in kwargs.items():
#                 if k in i.__dict__:
#                     if i.__dict__[k] != v:
#                         break
#                 # else:
#                 #     break
#             else:
#                 return i
#                 # return i.copy()
#         return None
#
#
# class ResMngEditMap(ResMng):
#     pass
#
#
# class ResMngShow(ResMng):
#     pass
#
#
# class ResMngMaker:
#     value = None
#     key = None
#
#     @classmethod
#     def init(cls, d0):
#         if d0 == cls.key:
#             return cls.value
#         if d0 == 'show':
#             obj = ResMngShow()
#         elif d0 == 'edit':
#             obj = ResMngEditMap()
#         elif d0 == 'mode':
#             obj = ResMngAdj()
#         cls.value = obj
#         return obj
#

resManager = ResMng()
from .unit import Shard, Spirit, UnitMaker
from .source import SourceMaker
from .mode import ModeMaker
