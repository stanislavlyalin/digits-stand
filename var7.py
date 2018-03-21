# -*- coding: utf-8 -*-
# Написать приложение, которое позволяет открыть изображение,
# рисовать на нем линии с помощью мыши и сохранить получившийся рисунок в файл.

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QBrush


class MyLabel(QLabel):

    def __init__(self, *args):
        super().__init__(*args)
        self.pressed = False
        
    def mousePressEvent(self, event):
        self.pressed = True
        self.xPrev = event.x()
        self.yPrev = event.y()

        self.painter = QPainter(self.pixmap())
        self.painter.begin(self)

    def mouseMoveEvent(self, event):
        if self.pressed:
            
            color = QColor(0, 0, 0)
            self.painter.setBrush(color)
            pen = QPen(color, 15)
            self.painter.setPen(pen)

            self.painter.drawLine(self.xPrev, self.yPrev, event.x(), event.y())
            
            self.xPrev = event.x()
            self.yPrev = event.y()
            self.repaint()

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.painter.end()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('var7.ui', self)

        self.image = MyLabel(self)
        self.pixmap = QPixmap('images/digit_background.png')
        self.image.setPixmap(self.pixmap)
        self.verticalLayout.insertWidget(0, self.image)
   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
