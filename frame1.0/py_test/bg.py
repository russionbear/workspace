#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :bg.py
# @Time      :2022/1/2 16:30
# @Author    :russionbear

from standard.render.background import TestWinEditor, TestWinTool
from standard.core import Core

# Core.add(TestWinEditor((800, 600), r'E:\TMP\policyGame\music'))
Core.add(TestWinTool((600, 400)))
Core.run()
