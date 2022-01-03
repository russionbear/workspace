#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :adjuster.py
# @Time      :2022/1/2 16:43
# @Author    :russionbear

# import sys
# print(sys.path)
# sys.path.append('E:\\workspace\\workspace\\frame1.0')
# print(sys.path)
# import standard
# print('fdfd')

from standard.resource.tool.madjuster import resManager, ModeAdjuster
from standard.core import Core

resManager.load_source(r'E:\workspace\workspace\test\source')
resManager.load_modes(r'E:\workspace\workspace\test\modes', 1)

Core.add(ModeAdjuster((800, 600)))
Core.run()
