## ---------------------------------------------------------------------------------------
## Main.py
## This is the primary function for the Elly application. Running this code launches Elly.
## This is also the target function for PyInstaller when building the .exe version of Elly.
## ---------------------------------------------------------------------------------------

# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sys

# Import the main GUI component
from widget_main import CentralWidget


# Defines a main window class - this is the application window
class MyMainWindow(QMainWindow):
    def __init__(self):
        # Allows access to other functions within the class
        super().__init__()       
        # Determines size of the window
        self.setGeometry(100, 100, 1500, 1500)
        # Sets application icon
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/logo_500x500.png')))
        # Sets application title
        self.setWindowTitle('Elly2')
        # Activates the menu bar
        self.initMenu()
        # Launches the central widget
        self.initCentralWidget()

    # Create and populate the top menu bar
    def initMenu(self):
        # Create top menu bar
        mainMenu = self.menuBar()
        # File subMenu
        fileMenu = mainMenu.addMenu('File')
        # Edit subMenu
        editMenu = mainMenu.addMenu('Edit')
        # Help subMenu
        helpMenu = mainMenu.addMenu('Help')

    # Launches the main widget of the GUI
    def initCentralWidget(self):
        self.myCentralWidget = CentralWidget()
        self.setCentralWidget(self.myCentralWidget)


# Function for launching the GUI
def main():
    global rect
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    rect = screen.availableGeometry()
    window = MyMainWindow()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
