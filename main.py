# -*- coding: utf-8 -*-
"""
Created on 19.11.2021 16:08 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-11-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import logging
import os
import sys
from PyQt5.QtWidgets import *

from src import MainWindow


def print_exceptions(etype, value, tb):
    import traceback
    text = "\n".join(traceback.format_exception(etype, value, tb))
    logging.error(text)
    traceback.format_exception(etype, value, tb)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[
                            logging.StreamHandler(sys.stdout)
                        ]
                        )
    app = QApplication(sys.argv)
    gui = MainWindow(dir=sys.argv[1])
    gui.model.setRootPath(os.getcwd())
    gui.show()

    sys.exit(app.exec_())
