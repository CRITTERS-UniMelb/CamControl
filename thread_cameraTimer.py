# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time

# Import local scripts


class CameraTimer(QThread):

    recordingSignal = pyqtSignal(object)

    def __init__(self, duration):
        super().__init__()
        self.duration = duration
    
    def initialization(self):
        self.recordingSignal.emit(True)
        self.timeInit = time.time()
    
    def run(self):
        self.timeCurrent = time.time()
        while self.timeCurrent - self.timeInit < self.duration:
            self.timeCurrent = time.time()
        self.recordingSignal.emit(False)
