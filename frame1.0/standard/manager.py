#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :manager.py
# @Time      :2021/12/19 10:34
# @Author    :russionbear


class A:
    def __init__(self):
        self.data = 100

    def abd(self):
        print(self.data)

    def __del__(self):
        print('del')


if __name__ == "__main__":
    a = A()
    func = a.abd
    del a
    func()
    print('dfdf')
