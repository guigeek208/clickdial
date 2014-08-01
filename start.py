# -*- coding: latin-1 -*-
import sys
from PyQt4 import QtGui
from ui_mainwindow import Ui_MainWindow

if __name__ == "__main__":  
    app = QtGui.QApplication(sys.argv)
    debug = True
    main = Ui_MainWindow(debug)
    main.show()
    sys.exit(app.exec_())
