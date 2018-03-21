# -*- coding: utf-8 -*-
# Написать приложение, которое позволяет открыть изображение,
# рисовать на нем линии с помощью мыши и сохранить получившийся рисунок в файл.

import sys
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QImage
from PyQt5.QtCore import QTimer


class MyLabel(QLabel):

    def __init__(self, *args):
        super().__init__(*args)
        self.pressed = False
        self.setFixedSize(200, 200)

        self.classifyTimer = QTimer()
        self.classifyTimer.timeout.connect(self.classify)

        # загрузка весов нейронной сети

    def mousePressEvent(self, event):
        self.pressed = True
        self.xPrev = event.x()
        self.yPrev = event.y()

        self.painter = QPainter(self.pixmap())
        self.painter.begin(self.pixmap())
        
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

        # запуск кода классификации картинки
        # QTimer.singleShot(1000, self.classify)
        # self.classifyTimer.stop()
        self.classifyTimer.start(2000)
        QTimer.singleShot(5000, self.clearImage)

    def classify(self):
        # классификация картинки
        print('Classify')
        self.classifyTimer.stop()

        # ресайз картинки
        small = self.pixmap().toImage().scaled(20, 20).convertToFormat(QImage.Format_Indexed8)
        s = small.bits().asstring(20*20)
        data = np.fromstring(s, dtype=np.int8).reshape((20, 20))
        print(data)
        small.save('test.png')


    def clearImage(self):
        self.painter.begin(self.pixmap())
        self.painter.eraseRect(0, 0, 200, 200)
        self.painter.end()
        self.repaint()

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
