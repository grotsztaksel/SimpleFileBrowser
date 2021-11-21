# -*- coding: utf-8 -*-
"""
Created on 19.11.2021 16:13 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__all__ = ['MainWindow']
__date__ = '2021-11-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import logging
import os
import typing
from random import random

from PyQt5 import uic
from PyQt5.QtCore import Qt, QModelIndex, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPalette
from PyQt5.QtWidgets import QFileSystemModel, QStyledItemDelegate, QStyleOptionViewItem, QFileDialog

from .dir_manager import DirManager
from .percent_bar import PercentBar
from .utils import isText

Ui_MainWindow, QMainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__), "mainwindow.ui"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags(), dir=None):
        super().__init__(parent, flags)
        self.setupUi(self)
        self.model = Model()
        self.mgr = None

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
        self.analyze(dir)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.setRootPath(dir))

    def analyze(self, dir):
        if self.mgr is not None and self.mgr.getDir() == dir:
            return
        logging.info(f"Starting dir manager for {dir}")
        self.mgr = DirManager(dir=dir)
        self.model.setDirManager(self.mgr)
        nf = self.mgr.dir.totalFiles()
        logging.info(f"Total number of files: {nf}.")
        progress_thresholds = list(range(0, nf, int(nf / 10)))
        progress_thresholds.pop(0)
        progress_thresholds.extend([nf, len(self.mgr.items)])  # The latter just in case progress reporting goes too far
        i = 0
        next_threshold = progress_thresholds.pop(0)
        for path, item in self.mgr.items.items():
            if not os.path.isfile(path):
                continue
            i += 1
            item.isBinary()
            if i >= next_threshold:
                logging.info("{0:0.0f}% done ({1:d} of {2:d})".format(100.0 * i / nf, i, nf))
                next_threshold = progress_thresholds.pop(0)


class Model(QFileSystemModel):
    """
    File system model that shows whether the file is binary or not
    """
    DATACOL = 1  # Column at which the custom data shall be presented

    TotalBinaryRole = Qt.UserRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cache = {}
        self.mgr = None

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        col = index.column()
        if role == Qt.ForegroundRole and not self.isDir(index):
            fp = self.filePath(index)
            if not self.isText(fp):
                # Make only non-text files (do not mark directories
                return QColor(Qt.blue).lighter()
            else:
                return super().data(index, role)
        elif role == Model.TotalBinaryRole and col == Model.DATACOL and self.mgr is not None:
            fp = os.path.normpath(self.filePath(index))
            if fp in self.mgr.items:
                return [self.mgr.items[fp].binCount(),
                        self.mgr.items[fp].binSize(),
                        self.mgr.items[fp].txtCount(),
                        self.mgr.items[fp].totalFiles()]
            else:
                pass
        return super().data(index, role)

    def setDirManager(self, manager):
        self.mgr = manager

    def isText(self, file):
        """
        Instead of interrogating the file every time on data() call, keep the information whether it is a text
        file in the cache once it has been checked
        """
        if file not in self.cache:
            self.cache[file] = isText(file)
        return self.cache[file]


class PercentBarDelegate(QStyledItemDelegate):
    """
    Delegate class that shows percentage of assessed files and how many of them are binary
    """

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        if self.percentBarRequired(index):
            bar = PercentBar()
            numbers = index.data(role=Model.TotalBinaryRole)
            if numbers:
                bar.numbers = numbers
            bar.paint(painter, option.rect)
        else:
            super().paint(painter, option, index)

    def percentBarRequired(self, index):
        """Helper function deciding whether the percent bar is required for given index"""
        return isinstance(index.model(), Model) and \
               index.model().isDir(index) and \
               index.column() == Model.DATACOL

