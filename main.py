# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sys

# Import local scripts
from widget_main import CentralWidget


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()       
        self.setGeometry(100, 100, 1500, 1500)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/logo_500x500.png')))
        self.setWindowTitle('Elly2')
        self.initMenu()
        self.initCentralWidget()

    def initMenu(self):
        # CREATING THE MENU
        mainMenu = self.menuBar()
        # File subMenu
        fileMenu = mainMenu.addMenu('File')
        # Edit subMenu
        editMenu = mainMenu.addMenu('Edit')
        # Help subMenu
        helpMenu = mainMenu.addMenu('Help')

    def initCentralWidget(self):
        self.myCentralWidget = CentralWidget()
        self.setCentralWidget(self.myCentralWidget)


# Main Function of the GUI
def main():
    global rect
    app = QApplication(sys.argv)
    # screen = app.primaryScreen()
    screen = app.screens()[0]
    rect = screen.availableGeometry()
    window = MyMainWindow()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
