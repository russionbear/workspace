# coding:utf-8
from standard.core import Core
from standard.mapEditor.bgEditor import MainView
from standard.mapEditor.blockEditor import BlockEditWin
from standard.mapEditor.win import WinStrategyEditor

from PyQt5.Qt import QApplication
from PyQt5 import QtCore, QtGui
import sys, functools, time, hashlib, shutil

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

Qapp = QApplication(sys.argv)

window = BlockEditWin((800, 600), (50, 50), (400, 400), r'E:\Date_code\py_data\policyGame\frame1.0\standard\run')
window.show()

sys.exit(Qapp.exec_())