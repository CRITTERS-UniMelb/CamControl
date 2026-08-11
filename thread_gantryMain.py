# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time

# Import local scripts
from thread_gantryCom import GantryCom
from thread_gantryAddCMD import GantryAddCMD


# Thread Class
class GantryMain(QThread):

    gantryConnectionSignal = pyqtSignal(int)
    gantryCurrentAction = pyqtSignal(object)
    gantryCoords = pyqtSignal(object)

    def __init__(self, gantryIP, gantryPort, gantryConnectionStatus):
        super(GantryMain, self).__init__()
        # Gantry address
        self.gantryAddress = (gantryIP, gantryPort)

        # Gantry connextion status
        self.gantryConnectionStatus = gantryConnectionStatus

    def run(self):
        # Starting the Gantry Communication Thread
        self.gantryCom = GantryCom(self.gantryAddress, self.gantryConnectionStatus)
        self.gantryCom.gantryConnectionSignal.connect(self.updateGantryConnectionStatus)
        self.gantryCom.gantryCoords.connect(self.updateGantryCoords)
        time.sleep(0.1)
        self.gantryCom.start()

        # Starting the Gantry Add CMD Thread
        self.gantryAddCMD = GantryAddCMD(self.gantryCom)
        self.gantryAddCMD.gantryAction.connect(self.updateGantryCurrentAction)
        time.sleep(0.1)
        self.gantryAddCMD.start()

        # Wait for all threads to exit
        self.gantryCom.wait()
        self.gantryAddCMD.wait()

    def newCommand(self, command):
        self.gantryAddCMD.addCMD(command)
    
    def stop(self):
        self.gantryAddCMD.stop()
        self.gantryCom.stop()
    
    def updateGantryConnectionStatus(self, status):
        self.gantryAddCMD.updateConnectionStatus(status)
        self.gantryConnectionSignal.emit(status)
    
    def updateGantryCurrentAction(self, action):
        self.gantryCurrentAction.emit(action)
    
    def updateGantryCoords(self, coords):
        self.gantryCoords.emit(coords)
    
