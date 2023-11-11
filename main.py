from main_window import MainWindow

import sys
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    # app
    app = QApplication(sys.argv)

    # main window
    window = MainWindow()
    window.show()

    # exit on quit
    sys.exit(app.exec())
