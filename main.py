# -*- coding: utf-8 -*-
# Написать приложение, которое позволяет открыть изображение,
# рисовать на нем линии с помощью мыши и сохранить получившийся рисунок в файл.

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
