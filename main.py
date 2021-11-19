# -*- coding: utf-8 -*-
"""
Created on 19.11.2021 16:08 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-11-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os
import sys
from PyQt5.QtWidgets import *

from src import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.model.setRootPath(os.getcwd())
    gui.show()

    sys.exit(app.exec_())

