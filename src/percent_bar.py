# -*- coding: utf-8 -*-
"""
Created on 19.11.2021 21:52 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

Custom widget used to display percentage of data analyzed and percentage of data fulfilling some criteria
"""

__all__ = ['PercentBar']
__date__ = '2021-11-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import Qt, QRect, pyqtSlot, QSize, QMargins, QPoint

from PyQt5.QtGui import QPaintEvent, QColor, QPen, QPainter
from PyQt5.QtWidgets import QWidget

try:
    from humanize import naturalsize

    HUMANSIZE_FOUND = True
except ImportError:
    HUMANSIZE_FOUND = False


class PercentBar(QWidget):
    def __init__(self, parent=None, tooltipFormat=None):
        super(PercentBar, self).__init__(parent)
        self.setMinimumSize(QSize(32, 16))
        self.numbers = 4 * [None]
        self.tf = "Analyzed: {}%\nTrue: {}%"

        self.unassessedColor = QColor(Qt.lightGray)
        self.assessedColor = QColor(Qt.white)
        self.trueColor = QColor(Qt.blue).lighter(180)
        self.textColor = QColor(Qt.black)

        if tooltipFormat is not None:
            self.setTooltipFormat(tooltipFormat)

    def setTooltipFormat(self, tf: str):
        """
        Sets the tooltip format
        :param tf:
        :return:
        """
        if not isinstance(tf, str):
            return
        self.tf = tf

    def paintEvent(self, e: QPaintEvent) -> None:
        rec = e.rect()
        painter = QPainter(self)
        self.paint(painter, rec)

    def paint(self, painter, rec0) -> None:
        painter.setPen(Qt.NoPen)
        b = painter.brush()
        b.setColor(self.unassessedColor)
        b.setStyle(Qt.SolidPattern)
        painter.setBrush(b)

        rec0 = rec0.marginsRemoved(QMargins(2, 2, 2, 2))
        rec = QRect(rec0)
        painter.drawRect(rec0)
        b.setColor(self.assessedColor)
        painter.setBrush(b)
        true = self.numbers[0]
        binSize = self.numbers[1]
        false = self.numbers[2]
        total = self.numbers[3]
        haveNumbers = isinstance(true, int) and isinstance(false, int) and isinstance(total, int)

        if haveNumbers:
            w = rec.width() * (true + false) / float(total)
            b.setStyle(Qt.SolidPattern)
        else:
            true = "?"
            total = "?"
            w = 0.25 * rec.width()
            b.setStyle(Qt.BDiagPattern)
        painter.setBrush(b)
        rec = QRect(rec.topLeft(), QSize(int(w), rec.height()))
        painter.drawRect(rec)
        b.setColor(self.trueColor)
        painter.setBrush(b)
        if haveNumbers:
            if true + false == 0:
                w = 0
            else:
                w = rec.width() * float(true) / (true + false)
            b.setStyle(Qt.SolidPattern)
        else:
            w = 0.25 * rec.width()
            b.setStyle(Qt.BDiagPattern)

        rec = QRect(rec.topLeft(), QSize(int(w), rec.height()))
        painter.drawRect(rec)

        pen = QPen()

        b.setColor(self.textColor)
        pen.setColor(self.textColor)
        pen.setStyle(Qt.SolidLine)
        pen.setBrush(b)
        pen.setColor(b.color())
        font = painter.font()
        font.setPixelSize(rec.height() * 0.8)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(pen)
        painter.setBrush(b)

        if isinstance(binSize, int):
            if HUMANSIZE_FOUND:
                size = naturalsize(binSize)
            else:
                size = binSize
        else:
            size = "?"

        leftText = f"{true} ({size})"
        painter.drawText(rec0, Qt.AlignLeft | Qt.AlignVCenter, leftText)
        painter.drawText(rec0, Qt.AlignRight | Qt.AlignVCenter, str(total))
