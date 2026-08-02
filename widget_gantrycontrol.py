# Import packages
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Import local scripts
import gantry_commands
import stylesheets
from thread_gantryMain import GantryMain


# Set up gantry control widget class
class GantryControlWidget(QGroupBox):

    # Set up signals for gantry connection, current action, and current location
    gantryConnectionSignal = pyqtSignal(int)
    gantryCurrentAction = pyqtSignal(object)
    gantryCoords = pyqtSignal(object)

    # Set initiation commands
    def __init__(self):
        # Give access to parent methods
        super().__init__()
        # Set initial gantry status to off
        self.gantryConnectionStatus = False
        # Set visual styles
        self.makeStylesheet()
        self.makeLayouts()
        self.makeFonts()
        self.makeIcon()
        self.makeTitle()
        self.makeInputs()
        self.makeButtons()

    # Define widget outline visuals
    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white;}
                """)

    # Define widget controls layout
    def makeLayouts(self):
        # Set main over-arching layout as a box
        self.widgetGantryControlsLayout = QHBoxLayout(self)

        # Add the icon to the main layout first - puts it at the left.
        self.gantryIconLayout = QVBoxLayout()
        self.gantryIconLayout.setAlignment(Qt.AlignVCenter)
        self.widgetGantryControlsLayout.addLayout(self.gantryIconLayout)

        # Add title and tnputs layout to the main layout
        self.gantryTitleInputsLayout = QVBoxLayout()
        self.widgetGantryControlsLayout.addLayout(self.gantryTitleInputsLayout)

        # Add title layout within the title and inputs layout (at top)
        self.gantryTitleLayout = QVBoxLayout()
        self.gantryTitleLayout.setAlignment(Qt.AlignTop)
        self.gantryTitleInputsLayout.addLayout(self.gantryTitleLayout, stretch=0)

        # Add inputs layout within the title and inputs layout (goes below title)
        self.gantryInputsLayout = QVBoxLayout()
        self.gantryInputsLayout.setAlignment(Qt.AlignVCenter)
        self.gantryTitleInputsLayout.addLayout(self.gantryInputsLayout, stretch=1)

        # Add a vertical line separator before the gantry buttons
        self.widgetGantryControlsLayout.addWidget(stylesheets.VLine())

        # Add gantry buttons to the main layout - puts it at right size
        self.gantryButtonsLayout = QHBoxLayout()
        self.gantryButtonsLayout.setAlignment(Qt.AlignVCenter)
        self.widgetGantryControlsLayout.addLayout(self.gantryButtonsLayout)

    # Method for setting application fonts
    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
        self.buttonFont = QFont("Sans Serif 10", 10)

    # Method for loading the gantry symbol
    def makeIcon(self):
        self.gantryIcon = QLabel()
        gantryIconQPixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/icons/gantry.png'))
        self.gantryIcon.setPixmap(gantryIconQPixmap)
        self.gantryIconLayout.addWidget(self.gantryIcon)

    # Method for formatting widgets title
    def makeTitle(self):
        # Set title
        self.gantryWidget_Title = QLabel("Gantry")
        # Set font to futura heavy
        self.gantryWidget_Title.setFont(QFont(self.futuraheavyfont_str, 16))
        # Place title into title layout 
        self.gantryTitleLayout.addWidget(self.gantryWidget_Title, alignment=Qt.AlignHCenter)

    # Method to define the input fields for the gantry
    def makeInputs(self):
        # IP entry
        # Create IP input box and add to parent inputs layout
        self.gantryWidget_GantryIPSettingsLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryIPSettingsLayout)
        # Create label, set size, and add to IP input box
        self.gantryWidget_GantryIPaddressLabel = QLabel("Gantry IP address:")
        self.gantryWidget_GantryIPaddressLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryIPSettingsLayout.addWidget(self.gantryWidget_GantryIPaddressLabel)
        # Add input field as editable line
        self.gantryWidget_GantryIPaddress = QLineEdit()
        self.gantryWidget_GantryIPaddress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Set default IP
        self.gantryWidget_GantryIPaddress.setText("192.168.3.11")
        # Add field to IP layout
        self.gantryWidget_GantryIPSettingsLayout.addWidget(self.gantryWidget_GantryIPaddress)

        # Port entry
        # Create port input box and add to parent inputs layout
        self.gantryWidget_GantryPortSettingsLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryPortSettingsLayout)
        # Create label, set size, and add to port input box
        self.gantryWidget_GantryPortLabel = QLabel("Gantry Port:")
        self.gantryWidget_GantryPortLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryPortSettingsLayout.addWidget(self.gantryWidget_GantryPortLabel)
        # Add input field as editable line
        self.gantryWidget_GantryPort = QLineEdit()
        self.gantryWidget_GantryPort.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Set default port
        self.gantryWidget_GantryPort.setText("3920")
        # Add field to port layout
        self.gantryWidget_GantryPortSettingsLayout.addWidget(self.gantryWidget_GantryPort)

        # X coord entry
        # Create x-coord input box and add to parent inputs layout
        self.gantryWidget_GantryXCoordLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryXCoordLayout)
        # Create label, set size, and add to xcoord input box
        self.gantryWidget_XCoordLabel = QLabel("Specify Gantry X coordinate:")
        self.gantryWidget_XCoordLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryXCoordLayout.addWidget(self.gantryWidget_XCoordLabel)
        # Add xcoord input at an interable number field
        self.gantryWidget_XCoord = QDoubleSpinBox()
        self.gantryWidget_XCoord.setEnabled(False)
        self.gantryWidget_XCoord.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Set limits on xcoord inputs
        self.gantryWidget_XCoord.setRange(0, 200)
        self.gantryWidget_XCoord.setSingleStep(10)
        self.gantryWidget_XCoord.setDecimals(2)
        # Set default value
        self.gantryWidget_XCoord.setValue(5.00)
        # Add field to xcoord layout
        self.gantryWidget_GantryXCoordLayout.addWidget(self.gantryWidget_XCoord)

        # Y coord entry
        # Create x-coord input box and add to parent inputs layout
        self.gantryWidget_GantryYCoordLayout = QHBoxLayout()
        self.gantryInputsLayout.addLayout(self.gantryWidget_GantryYCoordLayout)
        # Create label, set size, and add to xcoord input box
        self.gantryWidget_YCoordLabel = QLabel("Specify Gantry Y coordinate:")
        self.gantryWidget_YCoordLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gantryWidget_GantryYCoordLayout.addWidget(self.gantryWidget_YCoordLabel)
        # Add xcoord input at an interable number field
        self.gantryWidget_YCoord = QDoubleSpinBox()
        self.gantryWidget_YCoord.setEnabled(False)
        self.gantryWidget_YCoord.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Set limits on xcoord inputs
        self.gantryWidget_YCoord.setRange(0, 200)
        self.gantryWidget_YCoord.setSingleStep(10)
        self.gantryWidget_YCoord.setDecimals(2)
        # Set default value
        self.gantryWidget_YCoord.setValue(5.00)
        # Add field to xcoord layout
        self.gantryWidget_GantryYCoordLayout.addWidget(self.gantryWidget_YCoord)

    # Method to define the buttons for gantry controls
    def makeButtons(self):
        # Connect/Disconnect Gantry Button
        self.gantryWidget_ConnectButton = QPushButton()
        self.gantryWidget_ConnectButton.setText("Connect")
        self.gantryWidget_ConnectButton.setFont(self.buttonFont)
        self.gantryWidget_ConnectButton.setFixedHeight(100)
        self.gantryWidget_ConnectButton.setFixedWidth(100)
        self.gantryWidget_ConnectButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.gantryWidget_ConnectButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        # When clicked, run connectGantry function
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
        # When clicked, run resetGantry function
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
        # When clicked, run enableGantryMotors function
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
        # When clicked, run referenceGantryAxes function
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
        # When clicked, run moveGantry function
        self.gantryWidget_MoveGantryButton.clicked.connect(self.moveGantry)
        self.gantryButtonsLayout.addWidget(self.gantryWidget_MoveGantryButton)

    # Function to connect/disconnect to the gantry
    def connectGantry(self):
        # If gantry isn't connected, connect
        if (self.gantryConnectionStatus is False):
            # Set signal to 2
            self.gantryConnectionSignal.emit(2)
            # Set up a thread for the gantry connection, provide the IP, port, and status as inputs
            self.gantryThread = GantryMain(self.gantryWidget_GantryIPaddress.text(), int(self.gantryWidget_GantryPort.text()), self.gantryConnectionStatus)
            # Connect thread to gantry connection, action, and coords signal updates
            self.gantryThread.gantryConnectionSignal.connect(self.updateGantryConnectionStatus)
            self.gantryThread.gantryCurrentAction.connect(self.updateGantryCurrentAction)
            self.gantryThread.gantryCoords.connect(self.updateGantryCoords)
            # Launch thread
            self.gantryThread.start()
        # If gantry isn't connected, disconnect
        elif (self.gantryConnectionStatus is True):
            # Set signal to 3
            self.gantryConnectionSignal.emit(3)
            # Turn off thread
            self.gantryThread.stop()
            # Set status to false
            self.gantryConnectionStatus = False

    # Method for connecting the gantry, used when running programs rather than direct control
    def programConnectGantry(self):
        # First we check if gantry is already connected, if yes we pass, if not we connect it
        try:
            self.gantryThread.is_alive()
        except NameError:
            self.gantryConnectionStatus = False
            self.connectGantry()
        else:
            if (self.gantryConnectionStatus == False):
                self.connectGantry()
            else:
                pass

    # Method for disconnecting the gantry, used when running programs rather than direct control
    def programDisconnectGantry(self):
        # First we check if gantry is already connected, if yes we disconnect it, if not we pass
        try:
            self.gantryThread.is_alive()
        except NameError:
            pass
        else:
            if (self.gantryConnectionStatus == True):
                self.connectGantry()

    # Sends reset command to gantry
    def resetGantry(self):
        self.gantryThread.newCommand([gantry_commands.resetCMD,2])

    # Sends enable command to gantry
    def enableGantryMotors(self):
        self.gantryThread.newCommand([gantry_commands.enableMotorsCMD,2])

    # Sends command to move gantry to 5,5, reference axes, and reset
    def referenceGantryAxes(self):
        moveCMD = gantry_commands.moveTo(5,5)
        self.gantryThread.newCommand([moveCMD,20])
        self.gantryThread.newCommand([gantry_commands.referenceAxesCMD,20])
        self.gantryThread.newCommand([gantry_commands.resetCMD,2])
        self.gantryThread.newCommand([gantry_commands.enableMotorsCMD,2])

    # Sends command to move gantry to position
    def moveGantry(self):
        moveCMD = gantry_commands.moveTo(self.gantryWidget_XCoord.value(),self.gantryWidget_YCoord.value())
        self.gantryThread.newCommand([moveCMD,10])
    
    # Sends command to move gantry to position - used when running programs rather than direct control.
    def programMoveGantry(self, locations, movingTime):
        moveCMD = gantry_commands.moveTo(locations[0], locations[1])
        self.gantryThread.newCommand([moveCMD, movingTime])

    # Method for updating the gantry connection status and signal - activates/deactives gantry controls.
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

    # Method for updating the gantrys current action; when executing, disables buttons.
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

    # Method for updating the gantry coords
    def updateGantryCoords(self, coords):
        self.gantryCoords.emit(coords)
