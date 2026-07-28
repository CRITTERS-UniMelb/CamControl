# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import queue
import time

# Import local scripts
import gantry_commands

# Thread Class
class GantryAddCMD(QThread):

    gantryAction = pyqtSignal(object)

    def __init__(self, gantryCom):
        super(GantryAddCMD, self).__init__()
        # Gantry Com Thread
        self.gantryCom = gantryCom

        # Gantry connection Status
        self.gantryConnectionStatus = 0

        # End Gantry connection instruction
        self.endGantryConnection = False

        # Gantry command queue
        self.commandQueue = queue.Queue()


    def run(self):
        while self.endGantryConnection is False:
            try:
                command = self.commandQueue.get(False)
                if "CMD Reset" in str(command[0]):
                    self.gantryAction.emit("resetting")
                elif "CMD Enable" in str(command[0]):
                    self.gantryAction.emit("enabling")
                elif "CMD ReferenceAllJoints" in str(command[0]):
                    self.gantryAction.emit("referencing")
                elif "CMD Move" in str(command[0]):
                    self.gantryAction.emit("moving")
                self.gantryCom.sendCommand(command[0])
                self.commandQueue.task_done()
                time.sleep(command[1])
            except queue.Empty:
                if (self.gantryConnectionStatus == 1):
                    self.gantryAction.emit("none")
                elif (self.gantryConnectionStatus == 0):
                    self.gantryAction.emit("disconnected")
                time.sleep(0.1)
        time.sleep(0.1)
        self.gantryAction.emit("disconnected")
    

    def addCMD(self, command):
        self.commandQueue.put(command)

    
    def updateConnectionStatus(self, status):
        if (status == 0):
            self.gantryConnectionStatus = 0
        elif (status == 1):
            self.gantryConnectionStatus = 1


    def stop(self):
        self.endGantryConnection = True
