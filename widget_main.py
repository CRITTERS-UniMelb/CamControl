# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Import local scripts
from widget_gantrycontrol import GantryControlWidget
from widget_status import StatusWidget
from widget_cameracontrol import CameraControlWidget
from widget_arduinolightcontrol import ArduinoLightControlWidget
from widget_cameradisplay import CameraDisplayWidget
from widget_programcontrol import ProgramControlWidget

class CentralWidget(QWidget):

    maximizeSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.mainWidgetLayout = QGridLayout(self)

        self.initWidgets()
        self.makeSignalConnections()


    def initWidgets(self):
        self.widgetGantryControls = GantryControlWidget()
        self.mainWidgetLayout.addWidget(self.widgetGantryControls, 0, 0, 2, 5)

        self.widgetStatus = StatusWidget()
        self.mainWidgetLayout.addWidget(self.widgetStatus, 0, 5, 2, 5)

        self.widgetCameraControls = CameraControlWidget()
        self.mainWidgetLayout.addWidget(self.widgetCameraControls, 2, 0, 7, 4)

        self.widgetCameraDisplay = CameraDisplayWidget()
        self.mainWidgetLayout.addWidget(self.widgetCameraDisplay, 2, 4, 7, 6)

        self.widgetArduinoLightControls = ArduinoLightControlWidget()
        self.mainWidgetLayout.addWidget(self.widgetArduinoLightControls, 9, 0, 2, 3)

        self.widgetProgramControls = ProgramControlWidget()
        self.mainWidgetLayout.addWidget(self.widgetProgramControls, 9, 3, 2, 7)


    def makeSignalConnections(self):
        self.widgetGantryControls.gantryConnectionSignal.connect(self.updateGantryConnectionStatus)
        self.widgetGantryControls.gantryCurrentAction.connect(self.widgetStatus.updateGantryActionStatus)
        self.widgetGantryControls.gantryCoords.connect(self.widgetStatus.updateGantryCoords)

        # self.widgetCameraControls.cameraInitialisation.connect(self.widgetCameraDisplay.emitCameraDisplayDims)
        self.widgetCameraControls.cameraDisplayImage.connect(self.widgetCameraDisplay.updateCameraDisplayImage)
        self.widgetCameraControls.cameraShowHideDisplay.connect(self.updateCameraDisplayStatus)
        self.widgetCameraControls.cameraConnectionStatus.connect(self.updateCameraConnectionStatus)
        self.widgetCameraControls.cameraCurrentAction.connect(self.updateCameraCurrentAction)

        # self.widgetCameraDisplay.cameraDisplayDims.connect(self.updateCameraDisplayDims)
        self.widgetCameraDisplay.fullScreenSignal.connect(self.updateFullScreen)

        self.widgetArduinoLightControls.arduinoRingLightConnectionSignal.connect(self.widgetStatus.updateArduinoRingLightStatus)

        self.widgetProgramControls.programGantrySignal.connect(self.sendProgramGantrySignal)
        self.widgetProgramControls.programArduinoSignal.connect(self.sendProgramArduinoSignal)
        self.widgetProgramControls.programCameraSignal.connect(self.sendProgramCameraSignal)


    def updateGantryConnectionStatus(self, signal):
        self.widgetStatus.updateGantryConnectionStatus(signal)
        self.widgetProgramControls.updateGantryConnectionStatus(signal)


    def updateCameraConnectionStatus(self, signal):
        self.widgetStatus.updateCameraConnectionStatus(signal)
        self.widgetProgramControls.updateCameraConnectionStatus(signal)


    def updateCameraDisplayStatus(self, status):
        self.widgetCameraDisplay.showHideDisplayImage(status)
    
    def updateCameraCurrentAction(self, status):
        self.widgetStatus.updateCameraCurrentAction(status)
    
    # def updateCameraDisplayDims(self, dims):
    #     self.widgetCameraControls.updateCameraDisplayDims(dims)
    #     self.widgetCameraDisplay.updateCameraDisplayDims(dims)


    def sendProgramGantrySignal(self, signal):
        if (signal[0] == "Connect"):
            self.widgetGantryControls.programConnectGantry()
        elif (signal[0] == "Disconnect"):
            self.widgetGantryControls.programDisconnectGantry()
        elif signal[0] == "Reference":
            self.widgetGantryControls.resetGantry()
            self.widgetGantryControls.enableGantryMotors()
            self.widgetGantryControls.referenceGantryAxes()
        elif signal[0] == "Move":
            self.widgetGantryControls.programMoveGantry([signal[1], signal[2]], signal[3])
    
    def sendProgramArduinoSignal(self, signal):
        if (signal[0] == "Connect Arduino"):
            self.widgetArduinoLightControls.programConnectArduino()
        elif (signal[0] == "Turn Light On"):
            self.widgetArduinoLightControls.programSwitchLightOn()
        elif (signal[0] == "Turn Light Off"):
            self.widgetArduinoLightControls.programSwitchLightOff()
        elif (signal[0] == "Disconnect Arduino"):
            self.widgetArduinoLightControls.programDisconnectArduino()

    def sendProgramCameraSignal(self, signal):
        if signal[0] == "Connect Camera":
            self.widgetCameraControls.programConnectCamera()
        elif signal[0] == "Disconnect Camera":
            self.widgetCameraControls.programDisconnectCamera()
        elif signal[0] == "Start Video Recording":
            self.widgetCameraControls.programInitVideoRecord(signal)
        elif signal[0] == "Save Video":
            self.widgetCameraControls.programFinalizeVideoRecord(signal)


    def updateFullScreen(self, signal):
        if (signal == 1):
            self.widgetGantryControls.hide()
            self.widgetStatus.hide()
            self.widgetCameraControls.hide()
            self.widgetCameraDisplay.hide()
            self.widgetArduinoLightControls.hide()
            self.widgetProgramControls.hide()
            self.widgetCameraDisplay.restoreMaximizedGeometry()
            self.mainWidgetLayout.addWidget(self.widgetCameraDisplay, 0, 0, 11, 10)
            self.widgetCameraDisplay.show()
            self.widgetCameraDisplay.calculateMaximizedGeometry()
        elif (signal == 0):
            self.widgetCameraDisplay.hide()
            self.widgetGantryControls.show()
            self.widgetStatus.show()
            self.widgetCameraDisplay.show()
            self.widgetArduinoLightControls.show()
            self.widgetProgramControls.show()
            self.widgetCameraDisplay.restoreMinimizedGeometry()
            self.mainWidgetLayout.addWidget(self.widgetCameraDisplay, 2, 4, 7, 6)
            self.widgetCameraControls.show()
