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

from src.dir_manager import DirManager, DirTreeItem, Dir, File


class TestDirManager(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = prepareDirs()

    def tearDown(self) -> None:
        shutil.rmtree(self.dir)

    def test_getDir(self):
        mgr = DirManager(dir=self.dir)
        self.assertEqual(self.dir, mgr.getDir())


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
    files = [
        "d1/d1/d1/file1.txt",
        "d1/d1/d1/file2.txt",
        "d1/d1/d1/file3.dat",
        "d1/d2/file1.txt",
        "d1/d2/file2.dat",
        "d1/d2/d1/file1.dat",
        "d2/d1/d1/file1.txt"
    ]
    for file in files:
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
