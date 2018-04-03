# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from image import Image
from digit_image import DigitImage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Распознавание рукописных цифр')

        # создание виджетов
        self.inputImage = Image(self)
        self.pixmap = QPixmap('images/digit_background.png')
        self.inputImage.setPixmap(self.pixmap)

        self.inputCaption = QLabel('Напишите цифру')
        self.outputCaptionMLP = QLabel('Распознано MLP')
        self.outputCaptionCNN = QLabel('Распознано CNN')

        self.outputImageMLP = DigitImage(self)
        self.outputImageMLP.setPixmap(self.pixmap)

        self.outputImageCNN = DigitImage(self)
        self.outputImageCNN.setPixmap(self.pixmap)

        self.description = QLabel(self)
        self.description.setText(
            'Введённая вами цифра представляет собой картинку размером 200*200 '
            'пикселей. Картинка уменьшается до размера 20*20 = 400 пикселей. '
            'Эти значения поступают на вход полносвязной обученной нейронной '
            'сети. Сигнал проходит через входной слой, скрытый слой и попадает '
            'на выходной слой. В выходном слое 10 нейронов, так как '
            'распознаётся 10 цифр. Распознанная цифра будет на том выходе, '
            'значение функции активации на котором наибольшее.')
        self.description.setWordWrap(True)

        self.descriptionImage = QLabel(self)
        self.pixmap = QPixmap('images/description.png')
        self.descriptionImage.setPixmap(self.pixmap)

        # лэйауты
        self.vBox = QVBoxLayout()
        self.hBox = QHBoxLayout()
        self.vBoxInputImage = QVBoxLayout()
        self.vBoxOutputImageMLP = QVBoxLayout()
        self.vBoxOutputImageCNN = QVBoxLayout()

        # добавление виджетов в лэйауты
        self.setLayout(self.vBox)
        self.vBox.addLayout(self.hBox)

        self.vBoxInputImage.addWidget(self.inputCaption)
        self.vBoxInputImage.addWidget(self.inputImage)
        self.hBox.addLayout(self.vBoxInputImage)

        self.vBoxOutputImageMLP.addWidget(self.outputCaptionMLP)
        self.vBoxOutputImageMLP.addWidget(self.outputImageMLP)
        self.hBox.addLayout(self.vBoxOutputImageMLP)
        self.vBoxOutputImageCNN.addWidget(self.outputCaptionCNN)
        self.vBoxOutputImageCNN.addWidget(self.outputImageCNN)
        self.hBox.addLayout(self.vBoxOutputImageCNN)

        self.hBox.addWidget(self.description)
        self.vBox.addWidget(self.descriptionImage)

        # соединение сигнала и слота рисования цифры
        self.inputImage.classifiedMLP.connect(self.outputImageMLP.drawDigit)
        self.inputImage.clear.connect(self.outputImageMLP.clear)
        self.inputImage.classifiedCNN.connect(self.outputImageCNN.drawDigit)
        self.inputImage.clear.connect(self.outputImageCNN.clear)
