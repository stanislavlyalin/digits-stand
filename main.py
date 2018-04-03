# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
