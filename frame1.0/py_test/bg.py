#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :bg.py
# @Time      :2022/1/2 16:30
# @Author    :russionbear

from standard.render.background import TestWinEditor, TestWinShow
from standard.core import Core, Pen

# Core.add(TestWinEditor((800, 600),
#                        r'E:\TMP\policyGame\music',
#                        r'E:\workspace\workspace\test\names'))

Core.add(TestWinShow((800, 600), r'E:\TMP\policyGame\music'))
# Core.add(TestWinTool((600, 400)))
Core.run()
# print(Pen.to_std_size('fsdfsdfsdf987879'))
# print(Pen.get_width('111'))
