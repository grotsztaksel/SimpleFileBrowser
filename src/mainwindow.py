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

from .utils import isText

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
    DATACOL = 2  # Column at which the custom data shall be presented

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Add one data column
        :param parent: parent index
        :return:
        """
        return super(Model, self).columnCount() + 1

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> typing.Any:
        if section < Model.DATACOL:
            return super(Model, self).headerData(section, orientation, role)
        elif section == Model.DATACOL:
            if role == Qt.DisplayRole:
                return "My custom data"
        else:
            return super(Model, self).headerData(section - 1, orientation, role)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        col = index.column()
        if col == 0 and role == Qt.ForegroundRole:
            fp = self.filePath(index)
            if os.path.isfile(fp) and not isText(fp):
                # Make only non-text files (do not mark directories
                return QColor(Qt.blue).lighter()
            else:
                return super().data(index, role)
        elif col < Model.DATACOL:
            return super().data(index, role)
        elif col == Model.DATACOL:
            if role == Qt.DisplayRole:
                return "blala"
        elif col > Model.DATACOL:
            return super().data(index.siblingAtColumn(col - 1), role)
