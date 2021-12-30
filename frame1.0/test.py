# coding:utf-8
from standard.resource import resManager
from standard.core import Core
from standard.madjuster import ModeAdjuster
from standard.mapEditor.bgEditor import MainView
from standard.mapEditor.blockEditor import BlockEditWin, MapSurf, BlockEditor
from standard.mapEditor.win import WinStrategyEditor

from PyQt5.Qt import QApplication
from PyQt5 import QtCore, QtGui
import sys, functools, time, hashlib, shutil, re

resManager.load_source('../test/source', True)
resManager.load_modes('../test/modes', 2)
print(resManager.m[0].edit_path)
print(resManager.d)

# print(re.sub('-+', '-', '-----'))
print(re.match('1(-.*){1:}3-?.*', '1-2-3'))
# exit()

# Core.add(MainView(r'E:\TMP\policyGame'))
# Core.run()

# from .setting import strategy_map_type


# Core.add(BlockEditor(strategy_map_type['winSize'],
#                      strategy_map_type['blockSize'],
#                      strategy_map_type['mapSize']))
# Core.run()

# Qapp = QApplication(sys.argv)
#
# window = WinStrategyEditor(r'E:\TMP\policyGame\test')
# window.show()
#
# sys.exit(Qapp.exec_())

# print(hash(0))
# with open(r'E:\workspace\workspace\test\maps\test.json', 'w') as f:
#     import json
#     json.dump({1: 12}, f)
# Core.add(ModeAdjuster((800, 600)))
# Core.run()
# exit()

Qapp = QApplication(sys.argv)

window = BlockEditWin((800, 600), r'..\test\maps/test.json', True, (10, 10))
window.show()

sys.exit(Qapp.exec_())

# Core.add(BlockEditor((800, 600), MapSurf(None, (50, 50)), ''))
# Core.run()
