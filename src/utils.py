# -*- coding: utf-8 -*-
"""
Created on 19.11.2021 16:24 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

A module with general purpose utilities
"""
__all__ = ['isBinary']
__date__ = '2021-11-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

import os

textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))


def isBinary(file: str) -> bool:
    """
    Returns true, if a file is identified as a binary file.
    The implementation is based on https://stackoverflow.com/a/7392391

    :param file: file path
    :return: True, if the path is a path to a binary file, otherwise False
    """
    if not os.path.isfile(file):
        return False
    return is_binary_string(open(file, 'rb').read(1024))
