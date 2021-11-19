# -*- coding: utf-8 -*-
"""
Created on 19.11.2021 21:52 11
 
@author: Piotr Gradkowski <grotsztaksel@o2.pl>

Custom widget used to display percentage of data analyzed and percentage of data fulfilling some criteria
"""

__all__ = ['PercentBar']
__date__ = '2021-11-19'
__authors__ = ["Piotr Gradkowski <grotsztaksel@o2.pl>"]

from PyQt5.QtCore import Qt, QRect, pyqtSlot, QSize, QMargins

from PyQt5.QtGui import QPaintEvent, QColor, QPen, QPainter
from PyQt5.QtWidgets import QWidget


class PercentBar(QWidget):
    def __init__(self, parent=None, tooltipFormat=None):
        super(PercentBar, self).__init__(parent)
        self.setMinimumSize(QSize(32, 16))
        self.assessed = 0.0
        self.true = 0.0
        self.tf = "Analyzed: {}%\nTrue: {}%"

        self.unassessedColor = QColor(Qt.gray)
        self.assessedColor = QColor(Qt.white)
        self.trueColor = QColor(Qt.darkBlue).lighter(250)

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

    @pyqtSlot(float)
    def setPercentAssessed(self, p) -> None:
        """
        Set the number between 0.0 and 1.0 that tells what percent of available data has been assessed
        :param p:
        """
        if 0.0 <= p <= 1.0:
            self.assessed = p
            self.repaint()

    @pyqtSlot(float)
    def setPercentTrue(self, p) -> None:
        """
        Set the number between 0.0 and 1.0 that tells what percent of assessed data fulfills given criteria
        :param p:
        """
        if 0.0 <= p <= 1.0:
            self.true = p
            self.repaint()

    def paintEvent(self, e: QPaintEvent) -> None:
        rec = e.rect()
        painter = QPainter(self)
        self.paint(painter, rec)

    def paint(self, painter, rec) -> None:
        painter.setPen(Qt.NoPen)
        b = painter.brush()
        b.setColor(self.unassessedColor)
        b.setStyle(Qt.SolidPattern)
        painter.setBrush(b)

        rec = rec.marginsRemoved(QMargins(2, 2, 2, 2))
        painter.drawRect(rec)
        b.setColor(self.assessedColor)
        painter.setBrush(b)
        if self.assessed == 0:
            return
        w = rec.width() * self.assessed
        rec = QRect(rec.topLeft(), QSize(int(w), rec.height()))
        painter.drawRect(rec)
        b.setColor(self.trueColor)
        painter.setBrush(b)
        if self.true == 0.0:
            return
        w = rec.width() * self.true
        rec = QRect(rec.topLeft(), QSize(int(w), rec.height()))
        painter.drawRect(rec)
