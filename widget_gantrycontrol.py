# Import packages
from ctypes import alignment
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

# Import local scripts
from thread_gantryMain import GantryMain
import gantry_commands
import stylesheets

class GantryControlWidget(QGroupBox):

    gantryConnectionSignal = pyqtSignal(int)
    gantryCurrentAction = pyqtSignal(object)
    gantryCoords = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.gantryConnectionStatus = False

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
        self.widgetGantryControlsLayout = QHBoxLayout(self)

        # Icon Layout
        self.gantryIconLayout = QVBoxLayout()
        self.gantryIconLayout.setAlignment(Qt.AlignVCenter)
        self.widgetGantryControlsLayout.addLayout(self.gantryIconLayout)

        # Title and Inputs Layout
        self.gantryTitleInputsLayout = QVBoxLayout()
        self.widgetGantryControlsLayout.addLayout(self.gantryTitleInputsLayout)

        # Title Layout
        self.gantryTitleLayout = QVBoxLayout()
        self.gantryTitleLayout.setAlignment(Qt.AlignTop)
        self.gantryTitleInputsLayout.addLayout(self.gantryTitleLayout, stretch=0)

        # Inputs Layout
        self.gantryInputsLayout = QVBoxLayout()
        self.gantryInputsLayout.setAlignment(Qt.AlignVCenter)
        self.gantryTitleInputsLayout.addLayout(self.gantryInputsLayout, stretch=1)

        # Add a vertical line separator before the buttons
        self.widgetGantryControlsLayout.addWidget(stylesheets.VLine())

        # Buttons Layout
        self.gantryButtonsLayout = QHBoxLayout()
        self.gantryButtonsLayout.setAlignment(Qt.AlignVCenter)
        self.widgetGantryControlsLayout.addLayout(self.gantryButtonsLayout)


    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
        self.buttonFont = QFont("Sans Serif 10", 10)


    def makeIcon(self):
        self.gantryIcon = QLabel()
        gantryIconQPixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/icons/gantry.png'))
        # .scaled(
        #     QSize(100,100),
        #     aspectRatioMode=Qt.KeepAspectRatio
        #     )
        self.gantryIcon.setPixmap(gantryIconQPixmap)
        self.gantryIconLayout.addWidget(self.gantryIcon)


    def makeTitle(self):
        # Title
        self.gantryWidget_Title = QLabel("Gantry")
        self.gantryWidget_Title.setFont(QFont(self.futuraheavyfont_str, 16))
        self.gantryTitleLayout.addWidget(self.gantryWidget_Title, alignment=Qt.AlignHCenter)

    def makeInputs(self):
        # IP entry
        self.gantryWidget_GantryIPSettingsLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryIPSettingsLayout)

        self.gantryWidget_GantryIPaddressLabel = QLabel("Gantry IP address:")
        self.gantryWidget_GantryIPaddressLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryIPSettingsLayout.addWidget(self.gantryWidget_GantryIPaddressLabel)

        self.gantryWidget_GantryIPaddress = QLineEdit()
        self.gantryWidget_GantryIPaddress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gantryWidget_GantryIPaddress.setText("192.168.3.11")
        self.gantryWidget_GantryIPSettingsLayout.addWidget(self.gantryWidget_GantryIPaddress)

        # Port entry
        self.gantryWidget_GantryPortSettingsLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryPortSettingsLayout)

        self.gantryWidget_GantryPortLabel = QLabel("Gantry Port:")
        self.gantryWidget_GantryPortLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryPortSettingsLayout.addWidget(self.gantryWidget_GantryPortLabel)
        self.gantryWidget_GantryPort = QLineEdit()
        self.gantryWidget_GantryPort.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gantryWidget_GantryPort.setText("3920")
        self.gantryWidget_GantryPortSettingsLayout.addWidget(self.gantryWidget_GantryPort)

        # X coord entry
        self.gantryWidget_GantryXCoordLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryXCoordLayout)

        self.gantryWidget_XCoordLabel = QLabel("Specify Gantry X coordinate:")
        self.gantryWidget_XCoordLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryXCoordLayout.addWidget(self.gantryWidget_XCoordLabel)
        self.gantryWidget_XCoord = QDoubleSpinBox()
        self.gantryWidget_XCoord.setEnabled(False)
        self.gantryWidget_XCoord.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gantryWidget_XCoord.setRange(0, 200)
        self.gantryWidget_XCoord.setSingleStep(10)
        self.gantryWidget_XCoord.setDecimals(2)
        self.gantryWidget_XCoord.setValue(5.00)
        self.gantryWidget_GantryXCoordLayout.addWidget(self.gantryWidget_XCoord)

        # Y coord entry
        self.gantryWidget_GantryYCoordLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryYCoordLayout)

        self.gantryWidget_YCoordLabel = QLabel("Specify Gantry Y coordinate:")
        self.gantryWidget_YCoordLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryYCoordLayout.addWidget(self.gantryWidget_YCoordLabel)
        self.gantryWidget_YCoord = QDoubleSpinBox()
        self.gantryWidget_YCoord.setEnabled(False)
        self.gantryWidget_YCoord.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gantryWidget_YCoord.setRange(0, 200)
        self.gantryWidget_YCoord.setSingleStep(10)
        self.gantryWidget_YCoord.setDecimals(2)
        self.gantryWidget_YCoord.setValue(5.00)
        self.gantryWidget_GantryYCoordLayout.addWidget(self.gantryWidget_YCoord)


    def makeButtons(self):
        # Connect/Disconnect Gantry Button
        self.gantryWidget_ConnectButton = QPushButton()
        self.gantryWidget_ConnectButton.setText("Connect")
        self.gantryWidget_ConnectButton.setFont(self.buttonFont)
        self.gantryWidget_ConnectButton.setFixedHeight(100)
        self.gantryWidget_ConnectButton.setFixedWidth(100)
        self.gantryWidget_ConnectButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.gantryWidget_ConnectButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.gantryWidget_ConnectButton.clicked.connect(self.connectGantry)
        self.gantryButtonsLayout.addWidget(self.gantryWidget_ConnectButton)

        # Reset Gantry Button
        self.gantryWidget_ResetButton = QPushButton("Reset")
        self.gantryWidget_ResetButton.setFont(self.buttonFont)
        self.gantryWidget_ResetButton.setEnabled(False)
        self.gantryWidget_ResetButton.setFixedHeight(100)
        self.gantryWidget_ResetButton.setFixedWidth(100)
        self.gantryWidget_ResetButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.gantryWidget_ResetButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.gantryWidget_ResetButton.clicked.connect(self.resetGantry)
        self.gantryButtonsLayout.addWidget(self.gantryWidget_ResetButton)

        # Enable Gantry Motors Button
        self.gantryWidget_EnableMotorsButton = QPushButton("Enable")
        self.gantryWidget_EnableMotorsButton.setFont(self.buttonFont)
        self.gantryWidget_EnableMotorsButton.setEnabled(False)
        self.gantryWidget_EnableMotorsButton.setFixedHeight(100)
        self.gantryWidget_EnableMotorsButton.setFixedWidth(100)
        self.gantryWidget_EnableMotorsButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.gantryWidget_EnableMotorsButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.gantryWidget_EnableMotorsButton.clicked.connect(self.enableGantryMotors)
        self.gantryButtonsLayout.addWidget(self.gantryWidget_EnableMotorsButton)

        # Reference Gantry Axes Button
        self.gantryWidget_RefAxesButton = QPushButton("Align")
        self.gantryWidget_RefAxesButton.setFont(self.buttonFont)
        self.gantryWidget_RefAxesButton.setEnabled(False)
        self.gantryWidget_RefAxesButton.setFixedHeight(100)
        self.gantryWidget_RefAxesButton.setFixedWidth(100)
        self.gantryWidget_RefAxesButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.gantryWidget_RefAxesButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.gantryWidget_RefAxesButton.clicked.connect(self.referenceGantryAxes)
        self.gantryButtonsLayout.addWidget(self.gantryWidget_RefAxesButton)

        # Gantry Move Button
        self.gantryWidget_MoveGantryButton = QPushButton("Move")
        self.gantryWidget_MoveGantryButton.setFont(self.buttonFont)
        self.gantryWidget_MoveGantryButton.setEnabled(False)
        self.gantryWidget_MoveGantryButton.setFixedHeight(100)
        self.gantryWidget_MoveGantryButton.setFixedWidth(100)
        self.gantryWidget_MoveGantryButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.gantryWidget_MoveGantryButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.gantryWidget_MoveGantryButton.clicked.connect(self.moveGantry)
        self.gantryButtonsLayout.addWidget(self.gantryWidget_MoveGantryButton)


    def connectGantry(self):
        if (self.gantryConnectionStatus is False):
            self.gantryConnectionSignal.emit(2)
            self.gantryThread = GantryMain(self.gantryWidget_GantryIPaddress.text(), int(self.gantryWidget_GantryPort.text()), self.gantryConnectionStatus)
            self.gantryThread.gantryConnectionSignal.connect(self.updateGantryConnectionStatus)
            self.gantryThread.gantryCurrentAction.connect(self.updateGantryCurrentAction)
            self.gantryThread.gantryCoords.connect(self.updateGantryCoords)
            self.gantryThread.start()
        elif (self.gantryConnectionStatus is True):
            self.gantryConnectionSignal.emit(3)
            self.gantryThread.stop()
            self.gantryConnectionStatus = False


    def programConnectGantry(self):
        # First we check if gantry is already connected, if yes we pass, if not we connect it
        try:
            self.gantryThread
        except:
            self.gantryConnectionStatus = False
            self.connectGantry()
        else:
            if (self.gantryConnectionStatus == False):
                self.connectGantry()
            else:
                pass


    def programDisconnectGantry(self):
        # First we check if gantry is already connected, if yes we disconnect it, if not we pass
        try:
            self.gantryThread
        except:
            pass
        else:
            if (self.gantryConnectionStatus == True):
                self.connectGantry()


    def resetGantry(self):
        self.gantryThread.newCommand([gantry_commands.resetCMD,2])


    def enableGantryMotors(self):
        self.gantryThread.newCommand([gantry_commands.enableMotorsCMD,2])


    def referenceGantryAxes(self):
        moveCMD = gantry_commands.moveTo(5,5)
        self.gantryThread.newCommand([moveCMD,20])
        self.gantryThread.newCommand([gantry_commands.referenceAxesCMD,20])
        self.gantryThread.newCommand([gantry_commands.resetCMD,2])
        self.gantryThread.newCommand([gantry_commands.enableMotorsCMD,2])


    def moveGantry(self):
        moveCMD = gantry_commands.moveTo(self.gantryWidget_XCoord.value(),self.gantryWidget_YCoord.value())
        self.gantryThread.newCommand([moveCMD,10])
    
    def programMoveGantry(self, locations, movingTime):
        moveCMD = gantry_commands.moveTo(locations[0], locations[1])
        self.gantryThread.newCommand([moveCMD, movingTime])


    def updateGantryConnectionStatus(self, status):
        self.gantryConnectionSignal.emit(status)
        if (status == 0):
            self.gantryConnectionStatus = False
            self.gantryWidget_GantryIPaddress.setEnabled(True)
            self.gantryWidget_GantryPort.setEnabled(True)
            self.gantryWidget_ConnectButton.setText("Connect")
            self.gantryWidget_ResetButton.setEnabled(False)
            self.gantryWidget_EnableMotorsButton.setEnabled(False)
            self.gantryWidget_RefAxesButton.setEnabled(False)
            self.gantryWidget_XCoord.setEnabled(False)
            self.gantryWidget_YCoord.setEnabled(False)
            self.gantryWidget_MoveGantryButton.setEnabled(False)
            self.gantryThread.gantryAddCMD.stop()
        elif (status == 1):
            self.gantryConnectionStatus = True
            self.gantryWidget_GantryIPaddress.setEnabled(False)
            self.gantryWidget_GantryPort.setEnabled(False)
            self.gantryWidget_ConnectButton.setText("Disconnect")
            self.gantryWidget_ResetButton.setEnabled(True)
            self.gantryWidget_EnableMotorsButton.setEnabled(True)
            self.gantryWidget_RefAxesButton.setEnabled(True)
            self.gantryWidget_XCoord.setEnabled(True)
            self.gantryWidget_YCoord.setEnabled(True)
            self.gantryWidget_MoveGantryButton.setEnabled(True)


    def updateGantryCurrentAction(self, action):
        self.gantryCurrentAction.emit(action)
        if (action == "none"):
            self.gantryWidget_ResetButton.setEnabled(True)
            self.gantryWidget_EnableMotorsButton.setEnabled(True)
            self.gantryWidget_RefAxesButton.setEnabled(True)
            self.gantryWidget_XCoord.setEnabled(True)
            self.gantryWidget_YCoord.setEnabled(True)
            self.gantryWidget_MoveGantryButton.setEnabled(True)
        else:
            self.gantryWidget_ResetButton.setEnabled(False)
            self.gantryWidget_EnableMotorsButton.setEnabled(False)
            self.gantryWidget_RefAxesButton.setEnabled(False)
            self.gantryWidget_XCoord.setEnabled(False)
            self.gantryWidget_YCoord.setEnabled(False)
            self.gantryWidget_MoveGantryButton.setEnabled(False)


    def updateGantryCoords(self, coords):
        self.gantryCoords.emit(coords)
