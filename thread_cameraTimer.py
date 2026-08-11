# Import packages
import time

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

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
