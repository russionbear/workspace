#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :setting.py
# @Time      :2022/1/2 15:53
# @Author    :russionbear


"""setting manager"""
import re

import xlrd


class STUnit:
    Data = None
    Move = {}
    Convey = {}
    Atk = {}
    AtkValue = {}
    Officer = {}

    @classmethod
    def load(cls, path):
        cls.Data = xlrd.open_workbook(path)
        cls.Move = cls.sheet_to_json(cls.Data.sheet_by_name('move'))
        cls.Convey = cls.sheet_to_json(cls.Data.sheet_by_name('convey'))
        for k, v in cls.Convey.items():
            del v['re']

        cls.Atk = cls.sheet_to_json(cls.Data.sheet_by_name('re_atk'))
        for k, v in cls.Atk.items():
            del v['re']
        cls.AtkValue = cls.sheet_to_json(cls.Data.sheet_by_name('atk'))
        cls.Officer = cls.sheet_to_json(cls.Data.sheet_by_name('officer'))

    @classmethod
    def get_key(cls, s0, type_):
        table = cls.Data.sheet_by_name(type_)
        s0 = '-'.join(s0)
        res = table.col_values(2, 2)
        for i1, i in enumerate(res):
            if re.match(i, s0) is not None:
                return table.col_values(1, i1+2)
        return None

    @staticmethod
    def sheet_to_json(table):
        tmp_d = {}
        keys = table.row_values(0)

        for i in range(1, table.nrows):
            d0 = {}
            for j in range(1, table.ncols):
                d0[keys[j]] = table.cell_value(i, j)
            tmp_d[table.cell_value(i, 0)] = d0
        return tmp_d

    @classmethod
    def get_move(cls, foot, geo):
        return cls.Move[foot][geo]

    @classmethod
    def get_convey(cls, key):
        return cls.Convey[key]['max'], cls.Convey['key']['type']

    @classmethod
    def get_atk(cls, key, atr):
        return cls.Atk[key][atr]

    @classmethod
    def get_atk_value(cls, ak, df):
        return cls.AtkValue[ak][df]

    @classmethod
    def get_officer(cls, name, atr):
        return cls.Officer[name][atr]