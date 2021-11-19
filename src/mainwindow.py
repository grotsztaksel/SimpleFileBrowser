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
from random import random

from PyQt5 import uic
from PyQt5.QtCore import Qt, QModelIndex, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPalette
from PyQt5.QtWidgets import QFileSystemModel, QStyledItemDelegate, QStyleOptionViewItem, QFileDialog

from .percent_bar import PercentBar
from .utils import isText

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags(), dir=None):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.model = Model(self)

        self.treeView.setItemDelegate(PercentBarDelegate(self.treeView))
        if dir is not None:
            self.lineEdit.setText(dir)
            self.onTextAccepted()

    @pyqtSlot()
    def onDirButtonClicked(self):
        """Open a directory selection dialog"""
        if isinstance(self.treeView.model(), Model):
            root = self.treeView.model().rootPath()
        else:
            root = os.getcwd()
        dir = QFileDialog.getExistingDirectory(self, "Select root directory", root)
        if dir:
            self.setRootDir(dir)

    @pyqtSlot()
    def onTextAccepted(self):
        """Adjust path separators"""
        text = self.lineEdit.text().replace("\/", os.sep).replace("/", os.sep)
        self.lineEdit.setText(text)
        pal = self.palette()
        brush = pal.text()
        if os.path.isdir(text):
            self.setRootDir(text)
        elif not text:
            pass
        else:
            brush.setColor(QColor(Qt.red))
        pal.setColor(QPalette.Text, brush.color())
        self.lineEdit.setPalette(pal)

    def setRootDir(self, dir):
        """Helper function to set the root path on all widgets and the model"""
        self.lineEdit.setText(dir)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.setRootPath(dir))


class Model(QFileSystemModel):
    """
    File system model that shows whether the file is binary or not
    """
    DATACOL = 2  # Column at which the custom data shall be presented

    PercentageAssessedRole = Qt.UserRole + 1
    PercentageBinaryRole = Qt.UserRole + 2

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
                return "% of binary files"
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
        elif role == Model.PercentageBinaryRole and col == Model.DATACOL:
            return 0.9
        elif role == Model.PercentageAssessedRole and col == Model.DATACOL:
            return 0.6
        elif col > Model.DATACOL:
            return super().data(index.siblingAtColumn(col - 1), role)


class PercentBarDelegate(QStyledItemDelegate):
    """
    Delegate class that shows percentage of assessed files and how many of them are binary
    """

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        if self.percentBarRequired(index):
            bar = PercentBar()
            bar.assessed = index.data(role=Model.PercentageAssessedRole)
            bar.true = index.data(role=Model.PercentageBinaryRole)
            bar.paint(painter, option.rect)
        else:
            super().paint(painter, option, index)

    def percentBarRequired(self, index):
        """Helper function deciding whether the percent bar is required for given index"""
        return isinstance(index.model(), Model) and \
               os.path.isdir(index.model().filePath(index.siblingAtColumn(0))) and \
               index.column() == Model.DATACOL
