# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore


class DigitImage(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFixedSize(200, 200)
        self.setStyleSheet('border: 3px solid grey;')

    @pyqtSlot(int)
    def drawDigit(self, digit):
        print(digit)
        self.painter = QPainter(self.pixmap())
        self.painter.begin(self.pixmap())

        font = self.painter.font()
        font.setPointSize(60)
        self.painter.setFont(font)

        self.painter.drawText(self.rect(), QtCore.Qt.AlignCenter, str(digit))
        self.painter.end()
        self.repaint()

    @pyqtSlot()
    def clear(self):
        self.painter.begin(self.pixmap())
        self.painter.eraseRect(self.rect())
        self.painter.end()
        self.repaint()
