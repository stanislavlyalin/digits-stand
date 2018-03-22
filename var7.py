# -*- coding: utf-8 -*-
# Написать приложение, которое позволяет открыть изображение,
# рисовать на нем линии с помощью мыши и сохранить получившийся рисунок в файл.

import sys
import numpy as np
import scipy.io
from predict import predict
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QImage
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore


class MyLabel(QLabel):

    def __init__(self, *args):
        super().__init__(*args)
        self.pressed = False
        self.setFixedSize(200, 200)

        self.classifyTimer = QTimer()
        self.classifyTimer.timeout.connect(self.classify)

        # загрузка весов нейронной сети
        data = scipy.io.loadmat('weights.mat')
        self.Theta1 = np.matrix(data['Theta1'])
        self.Theta2 = np.matrix(data['Theta2'])


    def mousePressEvent(self, event):
        self.pressed = True
        self.xPrev = event.x()
        self.yPrev = event.y()

        self.painter = QPainter(self.pixmap())
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.begin(self.pixmap())
        
    def mouseMoveEvent(self, event):
        if self.pressed:
            
            color = QColor(0, 0, 0)
            self.painter.setBrush(color)
            pen = QPen(color, 15)
            pen.setCapStyle(QtCore.Qt.RoundCap)
            self.painter.setPen(pen)

            self.painter.drawLine(self.xPrev, self.yPrev, event.x(), event.y())
            
            self.xPrev = event.x()
            self.yPrev = event.y()
            self.repaint()

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.painter.end()

        # запуск кода классификации картинки
        self.classifyTimer.start(500)
        QTimer.singleShot(1000, self.clearImage)

    def classify(self):
        self.classifyTimer.stop()

        # ресайз картинки
        small = self.pixmap().toImage().scaled(20, 20).convertToFormat(QImage.Format_Grayscale8)
        s = small.bits().asstring(20*20)
        sample = np.fromstring(s, dtype=np.uint8)
        sample = sample.reshape((20, 20)).T.reshape((1, 400))
        sample = (255 - sample) / 243.0

        # предсказание с помощью классификатора
        pred = predict(self.Theta1, self.Theta2, sample)
        print('Digit is %d' % (pred[0] % 10))

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
