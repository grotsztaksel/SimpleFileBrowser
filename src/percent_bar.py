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


class PercentBar(QWidget):
    def __init__(self, parent=None, tooltipFormat=None):
        super(PercentBar, self).__init__(parent)
        self.setMinimumSize(QSize(32, 16))
        self.numbers = [2, 4, 7]
        self.tf = "Analyzed: {}%\nTrue: {}%"

        self.unassessedColor = QColor(Qt.lightGray)
        self.assessedColor = QColor(Qt.white)
        self.trueColor = QColor(Qt.darkGreen).lighter(120)
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
        false = self.numbers[1]
        total = self.numbers[2]

        w = rec.width() * (true + false) / float(total)
        rec = QRect(rec.topLeft(), QSize(int(w), rec.height()))
        painter.drawRect(rec)
        b.setColor(self.trueColor)
        painter.setBrush(b)
        w = rec.width() * float(true) / (true + false)
        rec = QRect(rec.topLeft(), QSize(int(w), rec.height()))
        painter.drawRect(rec)

        leftTextR = QRect(rec0.topLeft(), QSize(int(0.25 * rec0.width()), rec0.height()))
        rightTextR = QRect(QPoint(int(0.75 * rec0.width()), rec0.top()), rec0.bottomRight())

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

        painter.drawText(leftTextR, Qt.AlignLeft | Qt.AlignVCenter, str(true))
        painter.drawText(rightTextR, Qt.AlignRight | Qt.AlignVCenter, str(total))
