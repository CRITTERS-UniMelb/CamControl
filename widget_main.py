# Import packages
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Import sub-widgets for GUI
from widget_cameracontrol import CameraControlWidget
from widget_cameradisplay import CameraDisplayWidget
from widget_gantrycontrol import GantryControlWidget
from widget_programcontrol import ProgramControlWidget
from widget_status import StatusWidget


# Define core widget (containing all other widgets)
class CentralWidget(QWidget):

    # Declare signal for whether the window is maximized
    maximizeSignal = pyqtSignal(object)

    # Define behaviour on launch
    def __init__(self):
        # Give access to other methods in class
        super().__init__()
        # Setup layout for full GUI
        self.mainWidgetLayout = QGridLayout(self)
        # Initiate all widgets
        self.initWidgets()
        # Connect all signals between widgets/threads
        self.makeSignalConnections()

    # Function to launch all widgets, defines relative size
    def initWidgets(self):
        # Gantry control widget at top-left
        self.widgetGantryControls = GantryControlWidget()
        # Set gantry control widget size (order is top, left, height, width)
        self.mainWidgetLayout.addWidget(self.widgetGantryControls, 0, 0, 2, 5)

        # System status widget at top-right
        self.widgetStatus = StatusWidget()
        # Set system status widget size (order is top, left, height, width)
        self.mainWidgetLayout.addWidget(self.widgetStatus, 0, 5, 2, 5)

        # Camera control widget at centre-left
        self.widgetCameraControls = CameraControlWidget()
        # Set camera control widget size (order is top, left, height, width)
        self.mainWidgetLayout.addWidget(self.widgetCameraControls, 2, 0, 7, 4)

        # Camera display widget at centre-right
        self.widgetCameraDisplay = CameraDisplayWidget()
        # Set camera display widget size (order is top, left, height, width)
        self.mainWidgetLayout.addWidget(self.widgetCameraDisplay, 2, 4, 7, 6)

        # Program control widget at bottom 
        self.widgetProgramControls = ProgramControlWidget()
        # Set program control widget size (order is top, left, height, width); -1 for width makes it go all the way across
        self.mainWidgetLayout.addWidget(self.widgetProgramControls, 9, 0, 2, -1)


    # Make connections for signals between widgets and threads
    def makeSignalConnections(self):
        # Connect gantry control widget to gantry status and program control widgets for gantry connection status
        self.widgetGantryControls.gantryConnectionSignal.connect(self.updateGantryConnectionStatus)
        # Connect gantry control widget to gantry status widget for gantry actions and coordinates
        self.widgetGantryControls.gantryCurrentAction.connect(self.widgetStatus.updateGantryActionStatus)
        self.widgetGantryControls.gantryCoords.connect(self.widgetStatus.updateGantryCoords)

        # Connect camera control widget to camera display widget and program control widget for image status, 
        # camera connections, and camera actions
        self.widgetCameraControls.cameraDisplayImage.connect(self.widgetCameraDisplay.updateCameraDisplayImage)
        self.widgetCameraControls.cameraShowHideDisplay.connect(self.updateCameraDisplayStatus)
        self.widgetCameraControls.cameraConnectionStatus.connect(self.updateCameraConnectionStatus)
        self.widgetCameraControls.cameraCurrentAction.connect(self.updateCameraCurrentAction)

        # Connect camera display widget to full screen controls
        self.widgetCameraDisplay.fullScreenSignal.connect(self.updateFullScreen)

        # Connect program controls to gantry controls for sending commands
        self.widgetProgramControls.programGantrySignal.connect(self.sendProgramGantrySignal)
        self.widgetProgramControls.programCameraSignal.connect(self.sendProgramCameraSignal)

    # Method to connect gantry controls to status widget and program widget
    def updateGantryConnectionStatus(self, signal):
        self.widgetStatus.updateGantryConnectionStatus(signal)
        self.widgetProgramControls.updateGantryConnectionStatus(signal)

    # Method to connect camera control widget to status widget and program widget
    def updateCameraConnectionStatus(self, signal):
        self.widgetStatus.updateCameraConnectionStatus(signal)
        self.widgetProgramControls.updateCameraConnectionStatus(signal)

    # Method to connect camera control widget and camera control widget
    def updateCameraDisplayStatus(self, status):
        self.widgetCameraDisplay.showHideDisplayImage(status)
    
    # Method to connect camera control widget and status widget
    def updateCameraCurrentAction(self, status):
        self.widgetStatus.updateCameraCurrentAction(status)
    
    # Method for gantry buttons to send signals to gantry controls
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
    
    # Method for camera buttons to send signals to camera controls
    def sendProgramCameraSignal(self, signal):
        if signal[0] == "Connect Camera":
            self.widgetCameraControls.programConnectCamera()
        elif signal[0] == "Disconnect Camera":
            self.widgetCameraControls.programDisconnectCamera()
        elif signal[0] == "Start Video Recording":
            self.widgetCameraControls.programInitVideoRecord(signal)
        elif signal[0] == "Save Video":
            self.widgetCameraControls.programFinalizeVideoRecord(signal)

    # Method for making the camera display full-screen
    def updateFullScreen(self, signal):
        # When active: hides all widgets except camera display
        if (signal == 1):
            self.widgetGantryControls.hide()
            self.widgetStatus.hide()
            self.widgetCameraControls.hide()
            self.widgetCameraDisplay.hide()
            self.widgetProgramControls.hide()
            # Make camera display full-screen
            self.widgetCameraDisplay.restoreMaximizedGeometry()
            self.mainWidgetLayout.addWidget(self.widgetCameraDisplay, 0, 0, 11, 10)
            self.widgetCameraDisplay.show()
            self.widgetCameraDisplay.calculateMaximizedGeometry()
        # When inactive: hide camera display, restore all other widgets, then put camera display back at original size
        elif (signal == 0):
            self.widgetCameraDisplay.hide()
            self.widgetGantryControls.show()
            self.widgetStatus.show()
            self.widgetCameraDisplay.show()
            self.widgetProgramControls.show()
            self.widgetCameraDisplay.restoreMinimizedGeometry()
            self.mainWidgetLayout.addWidget(self.widgetCameraDisplay, 2, 4, 7, 6)
            self.widgetCameraControls.show()
