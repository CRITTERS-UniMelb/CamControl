# Import packages
from ctypes import alignment
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import time

# Import local scripts
import stylesheets
from thread_arduino import ArduinoThread

class ArduinoLightControlWidget(QGroupBox):

    arduinoRingLightConnectionSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.arduinoConnected = False
        self.arduinoLightOn = False
       
        self.makeStylesheet()
        self.makeLayouts()
        self.makeFonts()
        self.makeIcon()
        self.makeTitle()
        self.makeInputs()
        self.makeButtons()
    
    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white;}
                """)

    def makeLayouts(self):
        # Main Layout
        self.arduinoLightControlWidgetLayout = QHBoxLayout(self)

        # Icon Layout
        self.arduinoLightControlWidget_IconLayout = QHBoxLayout()
        self.arduinoLightControlWidget_IconLayout.setAlignment(Qt.AlignVCenter)
        self.arduinoLightControlWidgetLayout.addLayout(self.arduinoLightControlWidget_IconLayout)

        # Title & Inputs Layout
        self.arduinoLightControlWidget_TitleInputsLayout = QVBoxLayout()
        self.arduinoLightControlWidgetLayout.addLayout(self.arduinoLightControlWidget_TitleInputsLayout)

        # Title Layout
        self.arduinoLightControlWidget_TitleLayout = QVBoxLayout()
        self.arduinoLightControlWidget_TitleLayout.setAlignment(Qt.AlignTop|Qt.AlignCenter)
        self.arduinoLightControlWidget_TitleInputsLayout.addLayout(self.arduinoLightControlWidget_TitleLayout, stretch=0)

        # Input Layout
        self.arduinoLightControlWidget_InputsLayout = QVBoxLayout()
        self.arduinoLightControlWidget_InputsLayout.setAlignment(Qt.AlignVCenter)
        self.arduinoLightControlWidget_TitleInputsLayout.addLayout(self.arduinoLightControlWidget_InputsLayout, stretch=1)

        # Vertical line separator
        self.arduinoLightControlWidgetLayout.addWidget(stylesheets.VLine())

        # Buttons Layout
        self.arduinoLightControlWidget_ButtonsLayout = QHBoxLayout()
        self.arduinoLightControlWidget_ButtonsLayout.setAlignment(Qt.AlignVCenter)
        self.arduinoLightControlWidgetLayout.addLayout(self.arduinoLightControlWidget_ButtonsLayout)


    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
        self.buttonFont = QFont("Sans Serif 10", 10)


    def makeIcon(self):
        # Icon
        self.arduinoRingLightIcon = QLabel()
        arduinoRingLightQPixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/icons/arduinoringlight.png'))
        self.arduinoRingLightIcon.setPixmap(arduinoRingLightQPixmap)
        self.arduinoLightControlWidget_IconLayout.addWidget(self.arduinoRingLightIcon)


    def makeTitle(self):
        # Title
        # self.arduinoLightControl_TitleP1 = QLabel("Arduino")
        # self.arduinoLightControl_TitleP1.setFont(QFont(self.futuraheavyfont_str, 16))
        # self.arduinoLightControlWidget_TitleLayout.addWidget(self.arduinoLightControl_TitleP1, alignment=Qt.AlignCenter)

        self.arduinoLightControl_TitleP2 = QLabel("Ring Light")
        self.arduinoLightControl_TitleP2.setFont(QFont(self.futuraheavyfont_str, 16))
        self.arduinoLightControlWidget_TitleLayout.addWidget(self.arduinoLightControl_TitleP2, alignment=Qt.AlignCenter)

    def makeInputs(self):
        # ComboBoxes Layout
        self.arduinoLightControlWidget_InputsParametersLayout = QGridLayout()
        self.arduinoLightControlWidget_InputsParametersLayout.setAlignment(Qt.AlignVCenter)
        self.arduinoLightControlWidget_InputsLayout.addLayout(self.arduinoLightControlWidget_InputsParametersLayout)

        # Camera Selection
        self.arduinoWidget_COMSelectionLabel = QLabel("USB Port:")
        self.arduinoWidget_COMSelectionLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.arduinoLightControlWidget_InputsParametersLayout.addWidget(self.arduinoWidget_COMSelectionLabel, 0, 0, 1, 1, alignment=Qt.AlignTop)
        self.arduinoWidget_COMSelection = QComboBox()
        self.arduinoWidget_COMSelection.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.arduinoWidget_COMSelection.addItems(["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10"])
        self.arduinoWidget_COMSelection.setCurrentIndex(2)
        # self.arduinoWidget_COMSelection.currentIndexChanged.connect(self.arduinoCOMChanged)
        self.arduinoLightControlWidget_InputsParametersLayout.addWidget(self.arduinoWidget_COMSelection, 0, 1, 1, 1, alignment=Qt.AlignTop)


    def makeButtons(self):
        # Connect/Disconnect Arduino Button
        self.arduinoWidget_ConnectButton = QPushButton("Connect")
        self.arduinoWidget_ConnectButton.setFont(self.buttonFont)
        self.arduinoWidget_ConnectButton.setFixedHeight(100)
        self.arduinoWidget_ConnectButton.setFixedWidth(100)
        self.arduinoWidget_ConnectButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.arduinoWidget_ConnectButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.arduinoWidget_ConnectButton.clicked.connect(self.connectArduino)
        self.arduinoLightControlWidget_ButtonsLayout.addWidget(self.arduinoWidget_ConnectButton)

        # Swith Ring Light ON/OFF Button
        self.arduinoWidget_OnOffButton = QPushButton("Switch\nOn")
        self.arduinoWidget_OnOffButton.setEnabled(False)
        self.arduinoWidget_OnOffButton.setFont(self.buttonFont)
        self.arduinoWidget_OnOffButton.setFixedHeight(100)
        self.arduinoWidget_OnOffButton.setFixedWidth(100)
        self.arduinoWidget_OnOffButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.arduinoWidget_OnOffButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.arduinoWidget_OnOffButton.clicked.connect(self.switchOnOff)
        self.arduinoLightControlWidget_ButtonsLayout.addWidget(self.arduinoWidget_OnOffButton)
    

    def arduinoCOMChanged(self):
        self.arduino = ArduinoThread(self.arduinoWidget_COMSelection.currentText())
        self.arduino.initialization()
        time.sleep(2)
        self.arduinoConnected = True

    def connectArduino(self):
        if (self.arduinoConnected is False):
            self.arduino = ArduinoThread(self.arduinoWidget_COMSelection.currentText())
            self.arduino.arduinoRingLightConnectionSignal.connect(self.arduinoConnectionSignal)
            self.arduino.initialization()             
        else:
            try:
                self.arduino
            except:
                self.arduinoWidget_ConnectButton.setText("Connect")
            else:
                if (self.arduinoLightOn is True):
                    self.switchOnOff()
                    time.sleep(0.2)
                self.arduino.stop()
                

    def arduinoConnectionSignal(self, signal):
        if (signal == 1):
            self.arduino.start()
            self.arduinoConnected = True
            self.arduinoWidget_ConnectButton.setText("Disconnect")
            self.arduinoWidget_OnOffButton.setEnabled(True)
        elif (signal == 0) or (signal == 2):
            self.arduinoConnected = False
            self.arduinoWidget_ConnectButton.setText("Connect")
            self.arduinoWidget_OnOffButton.setEnabled(False)
        self.arduinoRingLightConnectionSignal.emit(signal)


    def programConnectArduino(self):
        if (self.arduinoConnected is False):
            self.connectArduino()
        else:
            pass

    def programDisconnectArduino(self):
        if (self.arduinoConnected is True):
            self.connectArduino()
        else:
            pass

    def switchOnOff(self):
        try:
            self.arduino
        except:
            pass
        else:
            if (self.arduinoLightOn is False):
                self.arduino.switchON()
                self.arduinoLightOn = True
                self.arduinoWidget_OnOffButton.setText("Switch\nOff")
            elif (self.arduinoLightOn is True):
                self.arduino.switchOFF()
                self.arduinoLightOn = False
                self.arduinoWidget_OnOffButton.setText("Switch\nOn")

    def programSwitchLightOn(self):
        if (self.arduinoLightOn is False):
            self.switchOnOff()
        else:
            pass
    
    def programSwitchLightOff(self):
        if (self.arduinoLightOn is True):
            self.switchOnOff()
        else:
            pass
   