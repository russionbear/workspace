#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :input.py
# @Time      :2022/1/4 21:04
# @Author    :russionbear

import pygame
from Pinyin2Hanzi import is_pinyin, dag, DefaultDagParams
from .. import Pen
import ctypes


__param = DefaultDagParams()
PATH_NUM = 20


def get_pinyin(s0):
    """
    将一段拼音，分解成一个个拼音
    :param s0: 匹配的字符串
    :return: 匹配到的拼音列表
    """
    for i1, i in enumerate(reversed(s0)):
        if i < 'a' or i > 'z':
            s0 = s0[-i1+1:]

    result = []

    if not s0:
        return result

    max_len = 6  # 拼音最长为6
    s0 = s0.lower()
    s0_len = len(s0)

    # 逆向匹配
    while True:
        matched = 0
        matched_word = ''
        if s0_len < max_len:
            max_len = s0_len
        for i in range(max_len, 0, -1):
            s = s0[(s0_len - i):s0_len]
            # 字符串是否在拼音表中
            # if s in pinyinLib:
            if is_pinyin(s):
                matched_word = s
                matched = i
                break
        # 未匹配到拼音
        if len(matched_word) == 0:
            break
        else:
            result.append(s)
            s0 = s0[:(s0_len - matched)]
            s0_len = len(s0)
            if s0_len == 0:
                break
    return list(reversed(result))


def get_word_by_pinyin(s0):
    rlt = []
    l0 = dag(__param, get_pinyin(s0), path_num=PATH_NUM)
    for i in l0:
        rlt.append(''.join(i.path))
    return rlt


class Input:
    def __init__(self, pen, width,
                 size=25, font='SimHei',
                 image=None, fg=(0, 200, 0)
                 ):
        self.legalEvents = {pygame.MOUSEBUTTONDOWN,
                           pygame.KEYDOWN,
                           pygame.KEYUP}
        # self.__suf = pygame.surface.Surface
        self.__bg = None
        self.__pen = pen
        if image is not None:
            self.__priBg = pygame.transform.scale(
                pygame.image.load(image),
                (width, size*2))
            self.__bg = self.__priBg.copy()
        else:
            self.__priBg = None
            self.__bg = pygame.surface.Surface((width, size))
        self.__anchor = 0, 0
        self.__fontSize = size
        self.__pencil = Pen.make_pen(size, font)

        self.__words = ' '
        self.__pinyinPoint = 0
        self.__SPoint = 0

        self.__waitWords = []
        self.__waitPoint = 0
        self.__maxWaitWords = 0
        # self.__wordsPoint = 0
        self.__maxFonts = width // size
        self.__width = width
        # self.__wordSuf = Pen.render(self.__words, fg)

        self.__click = pygame.time.Clock()
        self._sparkTime = 0

        self.__locked = False
        self.__isHanzi = False

        self.__downBackSpace = False
        self.__nowBsTime = 0
        # self.__bsHas = False

        self.__moveDirection = 0
        self.__moveTime = 0
        # self.__moveHas = False

        self.__downCtrl = False
        self.__downShift = False
        self.__downCaps = False

        # self.__enterBack = None
        self.__callBack = None
        self.__id = None

        self.adjust_inputer()
        # self.swap_english_inputer(not self.__isHanzi)

    def set_call_back(self, func, id_=None):
        self.__callBack = func
        self.__id = id_

    def update(self):
        self.__click.tick()
        if self.__downBackSpace:
            if self.__SPoint == 0:
                self.__downBackSpace = False
                return
            if self.__nowBsTime > 100:
                self.__words = self.__words[:self.__SPoint-1] + \
                               self.__words[self.__SPoint:]
                self.__SPoint -= 1
                if self.__isHanzi:
                    if self.__pinyinPoint >= self.__SPoint:
                        self.__pinyinPoint = self.__SPoint
                    else:
                        self.__waitPoint = 0
                        self.__waitWords = \
                            get_word_by_pinyin(self.__words[self.__pinyinPoint:self.__SPoint])

                self.__nowBsTime = 0
            self.__nowBsTime += self.__click.get_time()

        if self.__moveDirection:
            if self.__moveTime > 120:
                self.__moveTime = 0
                if self.__moveDirection > 0:
                    if self.__SPoint != 0:
                        cur = self.__SPoint
                        self.__SPoint -= 1
                        mid_h = '|' if self.__isHanzi else '_'
                        self.__words = self.__words[:self.__SPoint] + mid_h + \
                                       self.__words[self.__SPoint] + self.__words[cur + 1:]
                    else:
                        self.__moveDirection = 0
                else:
                    if self.__SPoint + 1 != len(self.__words):
                        cur = self.__SPoint
                        self.__SPoint += 1
                        mid_h = '|' if self.__isHanzi else '_'
                        self.__words = self.__words[:cur] + \
                                       self.__words[self.__SPoint] + mid_h + \
                                       self.__words[self.__SPoint+1:]
                    else:
                        self.__moveDirection = 0

                self.__pinyinPoint = self.__SPoint
                if self.__waitWords:
                    self.__waitWords.clear()
            self.__moveTime += self.__click.get_time()

        if self.__locked:
            # print(self._sparkTime, self.__click.get_time())
            if self._sparkTime > 800:
                self._sparkTime = 0
                # print(self.__SPoint, self.__words)
                if self.__words[self.__SPoint] != ' ':
                    self.__words = self.__words[:self.__SPoint] + ' ' + \
                        self.__words[self.__SPoint+1:]
                else:
                    mid_h = '|' if self.__isHanzi else '_'
                    self.__words = self.__words[:self.__SPoint] + mid_h + \
                        self.__words[self.__SPoint+1:]
            self._sparkTime += self.__click.get_time()

        # 没有图片时
        if not self.__priBg:
            rect = self.__pen.blit(self.__bg, self.__anchor)
            self.__bg.fill((0, 0, 0), rect.move(0, self.__fontSize))
            pygame.draw.rect(self.__pen, (100, 255, 100), rect.move(0, self.__fontSize), 2)
        else:
            anchor = self.__anchor[0], self.__anchor[1] + self.__fontSize
            self.__pen.blit(self.__bg, anchor)

        # if self.__locked:
        #     t_words = self.__pencil.\
        #         cut_by_size(self.__words, self.__width - self.__fontSize, True)
        #     if t_words != self.__words:
        #         t_words = '...' + t_words
        # else:
        #     t_words = self.__pencil.\
        #         cut_by_size(self.__words, self.__width - 3 * self.__fontSize // 2)
        #     if t_words != self.__words:
        #         t_words += '...'

        self.__pen.blit(self.__pencil.render(self.__words),
                        (self.__anchor[0], self.__anchor[1] + self.__fontSize))

        if self.__waitWords:
            width = 0
            tmp_rlt = ''
            for i1, i in enumerate(self.__waitWords[self.__waitPoint:]):
                s0 = str(i1+1) + i + ' '
                length1 = Pen.get_width(s0)
                if width + length1 > self.__width:
                    break
                width += length1
                tmp_rlt += s0
                self.__maxWaitWords = i1
            # print(width, tmp_rlt, self.__width)
            self.__pen.blit(self.__pencil.render(tmp_rlt), self.__anchor)

    def event(self, e1):
        # print(e1)
        if e1.type == pygame.MOUSEBUTTONDOWN:
            if e1.button == 1:
                if self.contains(e1.pos):
                    self.__locked = True
                else:
                    # print('fdfdf')
                    self.__locked = False
                    self.__words = self.__words[:-1] + ' '
            return

        if not self.__locked:
            return

        if e1.key == pygame.K_BACKSPACE:
            if e1.type == pygame.KEYDOWN:
                self.__downBackSpace = True
                self.__nowBsTime = 2000
            else:
                self.__downBackSpace = False

        elif e1.key == pygame.K_LSHIFT or e1.key == pygame.K_RSHIFT:
            if e1.type == pygame.KEYDOWN:
                self.__downShift = True
                self.swap_english_inputer(self.__isHanzi)
                # self.__isHanzi = not self.__isHanzi
                # if not self.__isHanzi:
                #     self.__waitWords.clear()
                # else:
                #     self.__pinyinPoint = self.__SPoint
            else:
                self.__downShift = False

        elif e1.key == pygame.K_LCTRL or e1.key == pygame.K_RCTRL:
            if e1.type == pygame.KEYDOWN:
                self.__downCtrl = True
            else:
                self.__downCtrl = False

        elif e1.key == pygame.K_LEFT:
            if e1.type == pygame.KEYDOWN:
                self.__moveTime = 2000
                self.__moveDirection = 1
            else:
                self.__moveDirection = 0
        elif e1.key == pygame.K_RIGHT:
            if e1.type == pygame.KEYDOWN:
                self.__moveTime = 2000
                self.__moveDirection = -1
            else:
                self.__moveDirection = 0

        elif e1.type == pygame.KEYDOWN:
            if e1.key == pygame.K_PAGEDOWN:
                self.scroll_page(False)
            elif e1.key == pygame.K_PAGEUP:
                self.scroll_page()
            elif e1.key == pygame.K_RETURN:
                self.input_enter()
            elif  e1.key == pygame.K_CAPSLOCK:
                self.__downCaps = not self.__downCaps
            else:
                try:
                    c0 = e1.unicode
                    ord(c0)
                except ValueError:
                    c0 = chr(e1.key)
                self.input_hanzi(c0)

    def move(self, x=0, y=0, pos=None):
        if pos:
            y, x = pos
        self.__anchor = y, x

    def get_pos(self):
        return self.__anchor

    def get_size(self):
        return self.__bg.get_size()

    def get_rect(self):
        return self.__bg.get_rect()

    def input_hanzi(self, s0):
        # if self.__downShift:
        #     print(s0)
        if self.__pencil.get_width(self.__words) >= self.__width:
            return
        if self.__waitWords:
            if '1' <= s0 <= '9' or s0 == ' ':
                if s0 == ' ':
                    s0 = 1
                # try:
                cur = int(s0)-1
                if cur > self.__maxWaitWords:
                    return
                s0 = self.__waitWords[cur+self.__waitPoint]
                self.__waitWords.clear()
                self.__words = self.__words[:self.__pinyinPoint] + s0 + self.__words[self.__SPoint:]
                self.__SPoint = self.__pinyinPoint = self.__pinyinPoint + len(s0)
                # self.__SPoint -= 1
                return
                    # self.__pinyinPoint
                    # self.__pinyinPoint = len(self.__words) + len(s0)
                # except (IndexError, ValueError):
                #     return
                #     # self.__pinyinPoint = len(self.__words)
                #     # self.__waitWords = 0
                #     pass
        # elif self.__pinyinPoint + 6 <= self.__SPoint and not self.__waitWords:
        #     self.__pinyinPoint += 6

        # self.__words = self.__words[:-1] + s0 + self.__words[-1]
        self.__words = self.__words[:self.__SPoint] + s0 + self.__words[self.__SPoint:]
        self.__SPoint += 1
        # print(self.__SPoint, '1111')

        if self.__isHanzi:
            self.__waitPoint = 0
            self.__waitWords = get_word_by_pinyin(self.__words[self.__pinyinPoint:self.__SPoint])
            # print(self.__waitWords, self.__pinyinPoint, self.__words)

    def input_enter(self):
        self.__waitWords.clear()
        if self.__callBack:
            self.__callBack(self.__id, self.__words)
        # self.__enterBack.slot()
        # print('fdfd')

    def scroll_page(self, up=True):
        if up:
            self.__waitPoint -= self.__maxWaitWords + 1
            if self.__waitPoint < 0:
                self.__waitPoint= 0
        else:
            if len(self.__waitWords) - self.__waitPoint <= self.__maxWaitWords:
                return
            self.__waitPoint += self.__maxWaitWords + 1
            # if self.__waitPoint >= len(self.__waitWords):
            #     self.__waitPoint = len(self.__waitWords) - 1

    def swap_english_inputer(self, t0=True):
        self.__isHanzi = not t0
        if not self.__isHanzi:
            self.__waitWords.clear()
        else:
            self.__pinyinPoint = self.__SPoint

    def adjust_inputer(self):
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        curr_window = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
        klid = user32.GetKeyboardLayout(thread_id)
        lid = klid & (2 ** 16 - 1)
        lid_hex = hex(lid)
        if lid_hex == 0x409:
            self.swap_english_inputer()
        else:
            self.swap_english_inputer(False)
        # print(lid_hex)

    def contains(self, pos):
        # print(pos, self.get_rect(), self.get_pos())
        return self.get_rect().move(self.__anchor[0], self.__anchor[1] + self.__fontSize).collidepoint(pos[0], pos[1])


class TestWin:
    def __init__(self, size):
        self.legalEvents = {pygame.KEYDOWN, pygame.KEYUP}
        self.suf = pygame.display.set_mode(size)
        self.input = Input(self.suf, 200)

    def update(self):
        self.suf.fill((0, 0, 0))
        self.input.update()

    def event(self, e0):
        if e0.type == pygame.KEYDOWN or e0.type == pygame.KEYUP:
            self.input.event(e0)

