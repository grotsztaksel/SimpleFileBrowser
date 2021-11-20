# -*- coding: utf-8 -*-
"""
Created on 20.11.2021 17:22 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>
"""

__date__ = '2021-11-20'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import shutil
import unittest
import os

from test.app import app
from PyQt5.QtWidgets import QFileSystemModel

from src.dir_manager import DirManager, DirTreeItem, Dir, File

FILES = [
    "d1/d1/d1/file1.txt",
    "d1/d1/d1/file2.txt",
    "d1/d1/d1/file3.dat",
    "d1/d2/file1.txt",
    "d1/d2/file2.dat",
    "d1/d2/d1/file1.dat",
    "d2/d1/d1/file1.txt"
]


class TestDirManager(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = prepareDirs()

    def tearDown(self) -> None:
        shutil.rmtree(self.dir)

    def test_getDir(self):
        mgr = DirManager(dir=self.dir)
        self.assertEqual(self.dir, mgr.getDir())

    def test_setModel(self):
        model = QFileSystemModel()
        app.processEvents()
        self.assertTrue(os.path.isdir(self.dir))
        rootIndex = model.setRootPath(self.dir)
        self.assertEqual(os.path.basename(self.dir), model.data(rootIndex))

        mgr = DirManager(dir=self.dir)
        mgr.setModel(model)

        for path, item in mgr.items.items():
            index = model.index(path)
            self.assertEqual(item, mgr.map[index])

        # Store the indexes to easily access them
        indexes = {}
        indexes["d1"] = model.index(0, 0, rootIndex)
        indexes["d1/d1"] = model.index(0, 0, indexes["d1"])
        indexes["d1/d1/d1"] = model.index(0, 0, indexes["d1/d1"])
        indexes["d1/d1/d1/file1.txt"] = model.index(0, 0, indexes["d1/d1/d1"])
        indexes["d1/d1/d1/file2.txt"] = model.index(1, 0, indexes["d1/d1/d1"])
        indexes["d1/d1/d1/file3.dat"] = model.index(2, 0, indexes["d1/d1/d1"])
        indexes["d1/d2"] = model.index(1, 0, indexes["d1"])
        indexes["d1/d2/d1"] = model.index(0, 0, indexes["d1/d2"])
        indexes["d1/d2/d1/file1.dat"] = model.index(0, 0, indexes["d1/d2/d1"])
        indexes["d1/d2/file1.txt"] = model.index(1, 0, indexes["d1/d2"])
        indexes["d1/d2/file2.dat"] = model.index(2, 0, indexes["d1/d2"])
        indexes["d2"] = model.index(1, 0, rootIndex)
        indexes["d2/d1"] = model.index(0, 0, indexes["d2"])
        indexes["d2/d1/d1"] = model.index(0, 0, indexes["d2/d1"])
        indexes["d2/d1/d1/file1.txt"] = model.index(0, 0, indexes["d2/d1/d1"])

        for path, index in indexes.items():
            fullpath = os.path.normpath(os.path.join(self.dir, os.sep.join(path.split("/"))))
            self.assertEqual(fullpath,
                             os.path.normpath(model.filePath(index)), path)

            self.assertEqual(mgr.map[index], mgr.items[fullpath])


class TestDirTreeItem(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = prepareDirs()

    def tearDown(self) -> None:
        shutil.rmtree(self.dir)


class TestDir(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = prepareDirs()

    def tearDown(self) -> None:
        shutil.rmtree(self.dir)

    def test__init__(self):
        mgr = DirManager(dir=self.dir)
        dir = Dir(self.dir, mgr)
        self.assertEqual([], dir.files)
        self.assertEqual(["d1", "d2"],
                         [os.path.basename(d.path) for d in dir.dirs])
        self.assertEqual(['d1'],
                         [os.path.basename(d.path) for d in dir.dirs[0].dirs[1].dirs])
        self.assertEqual(['file1.txt', 'file2.dat'],
                         [os.path.basename(d.path) for d in dir.dirs[0].dirs[1].files])

    def test_totalFiles(self):
        mgr = DirManager(dir=self.dir)
        dir = Dir(self.dir, mgr)
        self.assertEqual(7, dir.totalFiles())


class TestFile(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = prepareDirs()

    def tearDown(self) -> None:
        shutil.rmtree(self.dir)

    def test_checkIsBinary(self):
        mgr = DirManager(dir=self.dir)
        for path in mgr.items.keys():
            if path[-4:] == ".txt":
                file = File(path, mgr)
                self.assertFalse(file.isBinary())
            if path[-4:] == ".dat":
                file = File(path, mgr)
                self.assertTrue(file.isBinary())


def prepareDirs():
    dir = os.path.join(os.path.dirname(__file__), "testdir")

    for file in FILES:
        subpath = os.sep.join(file.split("/"))
        path = os.path.join(dir, subpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.isfile(path):
            continue
        if path[-3:] == "dat":
            with open(path, 'wb') as f:
                byte_arr = [120, 3, 255, 0, 100]
                binary_format = bytearray(byte_arr)
                f.write(binary_format)
        elif path[-3:] == "txt":
            with open(path, "w") as f:
                f.write("blabla")
    return dir


if __name__ == '__main__':
    unittest.main()
