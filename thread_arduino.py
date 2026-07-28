# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import serial

# Import local scripts


class ArduinoThread(QThread):

    arduinoRingLightConnectionSignal = pyqtSignal(object)

    def __init__(self, arduinoCOM):
        super().__init__()
        self.arduinoCOM = str(arduinoCOM)
        self.arduinoSignal = False
        self.switched = False
        self.stopArduino = False
    
    def initialization(self):
        try:
            self.arduino = serial.Serial(port = self.arduinoCOM, timeout = 0)
        except:
            print("ELLY:    Couldn't initialize connection to the Arduino (Ring-Light)")
            self.arduinoRingLightConnectionSignal.emit(2)  # 2 = connection fails
        else:
            print("ELLY:    Successfully connected to the Arduino (Ring-Light)")
            time.sleep(1.5)
            self.arduinoRingLightConnectionSignal.emit(1)  # 1 = connection successful
    
    def stop(self):
        self.stopArduino = True

    def switchON(self):
        self.switched = True
        self.arduinoSignal = True
    
    def switchOFF(self):
        self.switched = True
        self.arduinoSignal = False
    
    def run(self):
        while self.stopArduino is False:
            if self.switched is True:
                if self.arduinoSignal is True:
                    self.arduino.write(str.encode('1'))
                else:
                    self.arduino.write(str.encode('0'))
                self.switched = False
            time.sleep(0.1)
        self.arduinoSignal = False
        self.switched = False
        self.arduinoRingLightConnectionSignal.emit(0)  # 0 = disconnected
        try:
            self.arduino
        except:
            pass
        else:
            self.arduino.close()
        print("ELLY:    Arduino (Ring-Light) disconnected")
