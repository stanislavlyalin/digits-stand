# -*- coding: utf-8 -*-
# Написать приложение, которое позволяет открыть изображение,
# рисовать на нем линии с помощью мыши и сохранить получившийся рисунок в файл.

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor


class MyLabel(QLabel):

    def __init__(self, *args):
        super().__init__(*args)
        self.pressed = False
        
    def mousePressEvent(self, event):
        self.pressed = True

    def mouseMoveEvent(self, event):
        if self.pressed:
            self.painter = QPainter(self.pixmap())
            color = QColor(128, 128, 128)
            self.painter.setBrush(color)
            self.painter.setPen(color)
            self.painter.drawEllipse(event.x(), event.y(), 5, 5)
            self.repaint()

    def mouseReleaseEvent(self, event):
        self.pressed = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('var7.ui', self)

        self.image = MyLabel(self)
        self.pixmap = QPixmap('images/digit_background.png')
        self.image.setPixmap(self.pixmap)
        self.verticalLayout.insertWidget(0, self.image)

        self.pushButton.clicked.connect(self.save_image)

    def save_image(self):
        filename = QFileDialog.getSaveFileName(self, 'Задайте путь сохранения файла', 'D:\\', 'PNG Image (*.png)')[0]
        self.image.pixmap().save(filename)
        QMessageBox.information(self, 'Информация', 'Изображение сохранено в файле ' + filename)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
