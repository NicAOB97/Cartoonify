# PYQT Trial 
# BUILDING A SCREEN
from PyQt5.QtWidgets import  QApplication
import sys

from classes import crtnfyApp

if __name__ == '__main__':
    # create application object
    app = QApplication(sys.argv)

    windows = crtnfyApp()
    windows.show()  

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing window...')

