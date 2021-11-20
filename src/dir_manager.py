# -*- coding: utf-8 -*-
"""
Created on 20.11.2021 00:57 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

Class responsible for analyzing the given directory (and subdirectories) with regard to whether files are binary or not.
Also keeps information about the percentage of binary files and percentage of accomplished analyses
"""

__all__ = ['DirManager']
__date__ = '2021-11-20'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import logging
import os

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileSystemModel

from src.utils import isText


class DirManager(QObject):
    """A class that collects the information about file tree and manages the files and directories"""

    def __init__(self, parent=None, dir=None):
        assert os.path.isdir(dir)
        super().__init__(parent)
        self.items = {}
        self.dir = None
        self.model = None
        self.map = {}
        self.setDir(dir)

    def setDir(self, dir):
        if not isinstance(dir, str):
            return
        if not os.path.isdir(dir):
            return
        self.dir = Dir(dir, self)

    def getDir(self):
        """Return the own path"""
        return self.dir.path

    def setModel(self, model):
        assert isinstance(model, QFileSystemModel)
        self.model = model
        for path, item in self.items.items():
            index = self.model.index(path)
            self.map[index] = item


class DirTreeItem:
    """Abstract class for directory tree items (directories, files etc)"""

    def __init__(self, basepath, manager):
        logging.debug(f"adding {type(self)}: {basepath}")
        self.path = basepath
        self.manager = manager
        self.manager.items[self.path] = self


class Dir(DirTreeItem):
    def __init__(self, basepath, manager):
        super().__init__(basepath, manager)
        self.dirs = []
        self.files = []
        try:
            subdirs = os.listdir(self.path)
        except (PermissionError, FileNotFoundError) as e:
            err = str(type(e))[:-2].rsplit("'", 1)[1]
            logging.debug(f"{err}: {self.path}")
            return
        for item in subdirs:
            path = os.path.join(self.path, item)
            if os.path.isfile(path):
                self.files.append(File(path, self.manager))
            elif os.path.isdir(path):
                self.dirs.append(Dir(path, self.manager))

    def totalFiles(self):
        """
        Returns the total number of files in this and child directories
        """
        return len(self.files) + sum([d.totalFiles() for d in self.dirs])


class File(DirTreeItem):
    def __init__(self, basepath, manager):
        super().__init__(basepath, manager)
        self.binary = None

    def isBinary(self):
        """
        Check whether the file is a binary one.
        :return:
        """
        if not isinstance(self.binary, bool):
            self.binary = not isText(self.path)
        return self.binary
