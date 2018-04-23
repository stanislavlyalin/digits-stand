# -*- coding: utf-8 -*-

import numpy as np
import scipy.io
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5 import QtCore
from predict import predict
from keras.models import model_from_json
from keras.optimizers import Adam
import h5py


class Image(QLabel):
    classifiedMLP = pyqtSignal(int)
    classifiedCNN = pyqtSignal(int)
    clear = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.pressed = False
        self.setFixedSize(200, 200)
        self.setStyleSheet('border: 3px solid grey;')

        self.classifyTimer = QTimer()
        self.classifyTimer.timeout.connect(self.classify)

        # загрузка весов нейронной сети MLP
        data = scipy.io.loadmat('weights.mat')
        self.Theta1 = np.matrix(data['Theta1'])
        self.Theta2 = np.matrix(data['Theta2'])

        # инициализация модели CNN
        jsonFile = open('model.json', 'r')
        loadedModelJson = jsonFile.read()
        jsonFile.close()
        self.cnnModel = model_from_json(loadedModelJson)
        self.cnnModel.load_weights('model.h5')
        self.cnnModel.compile(loss="categorical_crossentropy",
                              optimizer=Adam(),
                              metrics=["accuracy"])

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
        self.classifyTimer.start(1000)
        QTimer.singleShot(2000, self.clearImage)

    def classify(self):
        self.classifyTimer.stop()

        # предсказание с помощью MLP
        self.classifiedMLP.emit(self.classifyMLP())

        # предсказание с помощью свёрточной сети Keras
        self.classifiedCNN.emit(self.classifyCNN())

    def classifyMLP(self):
        # подготовка картинки к классификации
        small = self.pixmap().toImage().scaled(20, 20).convertToFormat(
            QImage.Format_Grayscale8)
        s = small.bits().asstring(20 * 20)
        sample = np.fromstring(s, dtype=np.uint8)
        sample = sample.reshape((20, 20)).T.reshape((1, 400))
        sample = (255 - sample) / 243.0

        # предсказание с помощью классификатора
        return predict(self.Theta1, self.Theta2, sample)[0] % 10

    def classifyCNN(self):
        # подготовка картинки к классификации
        small = self.pixmap().toImage().scaled(28, 28).convertToFormat(
            QImage.Format_Grayscale8)
        s = small.bits().asstring(28 * 28)
        sample = np.fromstring(s, dtype=np.uint8)
        sample = (255 - sample) / 255
        sample = sample.reshape((1, 1, 28, 28))

        # предсказание с помощью классификатора
        return np.argmax(self.cnnModel.predict(sample))


    def clearImage(self):
        self.painter.begin(self.pixmap())
        self.painter.eraseRect(self.rect())
        self.painter.end()
        self.repaint()
        self.clear.emit()
