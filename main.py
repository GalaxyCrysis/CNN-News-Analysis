from Gui import NewsTicker
from PyQt4 import QtGui
import sys

#start program
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = NewsTicker()
    app.exec()
