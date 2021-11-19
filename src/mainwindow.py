# -*- coding: utf-8 -*-
"""
Created on 19.11.2021 16:13 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['MainWindow']
__date__ = '2021-11-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os
import typing

from PyQt5 import uic
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileSystemModel

from .utils import isBinary

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.model = Model(self)

        self.treeView.setModel(self.model)


class Model(QFileSystemModel):
    """
    File system model that shows whether the file is binary or not
    """

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        if role == Qt.BackgroundRole:
            if isBinary(self.filePath(index)):
                return QColor(Qt.blue).lighter()
        return super().data(index, role)
