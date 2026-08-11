# Import packages
import os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import functions
import stylesheets

# Import local scripts
from thread_program import ProgramThread


# Define program control widget GUI box
class ProgramControlWidget(QGroupBox):

    # Declare program signals for gantry and camera
    programGantrySignal = pyqtSignal(object)
    programCameraSignal = pyqtSignal(object)

    # Define launch behaviour
    def __init__(self):
        super().__init__()
        self.timesLoaded = False
        self.timesDF = None
        self.locationsLoaded = False
        self.moveCommands = None
        self.gantryConnected = False
        self.cameraConnected = False

        self.makeStylesheet()
        self.makeLayouts()
        self.makeFonts()
        self.makeDirectories()
        self.makeIcon()
        self.makeTitle()
        self.makeInputs()
        self.makeButtons()

    # Function to define box style
    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white}
                """)

    # Function to set-up GUI layout
    def makeLayouts(self):
        # Main Layout
        self.programWidget_Layout = QHBoxLayout(self)

        # Icon Layout
        self.programWidget_IconLayout = QVBoxLayout()
        self.programWidget_IconLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_IconLayout)

        # Title and Device Selector Layout
        self.programWidget_TitleDeviceSelectorLayout = QVBoxLayout()
        self.programWidget_Layout.addLayout(self.programWidget_TitleDeviceSelectorLayout, stretch=1)

        # Title Layout
        self.programWidget_TitleLayout = QVBoxLayout()
        self.programWidget_TitleLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.programWidget_TitleDeviceSelectorLayout.addLayout(self.programWidget_TitleLayout, stretch=0)

        # Device Selector Layout
        self.programWidget_DeviceSelectorLayout = QVBoxLayout()
        self.programWidget_DeviceSelectorLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.programWidget_TitleDeviceSelectorLayout.addLayout(self.programWidget_DeviceSelectorLayout, stretch=1)

        # Vertical line separator 
        self.programWidget_Layout.addWidget(stylesheets.VLine())

        # Device Parameters Layout
        self.programWidget_DeviceParametersLayout = QVBoxLayout()
        self.programWidget_DeviceParametersLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_DeviceParametersLayout, stretch=2)

        # Vertical line separator 
        self.programWidget_Layout.addWidget(stylesheets.VLine())

        # Loading Buttons Layout
        self.programWidget_LoadingButtonsLayout = QHBoxLayout()
        self.programWidget_LoadingButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_LoadingButtonsLayout)

        # Vertical line separator 
        self.programWidget_Layout.addWidget(stylesheets.VLine())

        # Operating Buttons Layout
        self.programWidget_OperatingButtonsLayout = QHBoxLayout()
        self.programWidget_OperatingButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_OperatingButtonsLayout)

    # Function for GUI fonts
    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        futuralightfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Light font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
        self.futuralightfont_str = QFontDatabase.applicationFontFamilies(futuralightfont)[0]
        self.buttonFont = QFont(self.futuralightfont_str, 10)

    # Function to create output directory
    def makeDirectories(self):
        self.videoPath = os.path.join(os.path.dirname(__file__), 'videos')
        if not os.path.exists(self.videoPath):
            os.makedirs(self.videoPath)
        self.cameraOutputVideoDirectory = self.videoPath

    # Icon for program GUI
    def makeIcon(self):
        self.programIcon = QLabel()
        programIconQPixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/icons/program.png'))
        self.programIcon.setPixmap(programIconQPixmap)
        self.programWidget_IconLayout.addWidget(self.programIcon)

    # Function for GUI title block
    def makeTitle(self):
        # Title
        self.programWidget_Title = QLabel("Program")
        self.programWidget_Title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.programWidget_Title.setFont(QFont(self.futuraheavyfont_str, 16))
        self.programWidget_TitleLayout.addWidget(self.programWidget_Title, alignment=Qt.AlignmentFlag.AlignCenter)

    # Function for GUI input optionss
    def makeInputs(self):
        # Device selections
        self.programWidget_UseGantry = QCheckBox("Use Gantry")
        self.programWidget_UseGantry.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.programWidget_UseGantry.setChecked(True)
        # Connect to updateUseGantry function
        self.programWidget_UseGantry.stateChanged.connect(self.updateUseGantry)
        self.programWidget_DeviceSelectorLayout.addWidget(self.programWidget_UseGantry, alignment=Qt.AlignmentFlag.AlignCenter)

        self.programWidget_UseCamera = QCheckBox("Use Camera")
        self.programWidget_UseCamera.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.programWidget_UseCamera.setChecked(True)
        # Connect to updateUseCamera function
        self.programWidget_UseCamera.stateChanged.connect(self.updateUseCamera)
        self.programWidget_DeviceSelectorLayout.addWidget(self.programWidget_UseCamera, alignment=Qt.AlignmentFlag.AlignCenter)

        # Device Parameters
        ## Horizontal separator
        self.programWidget_DeviceParametersLayout.addWidget(stylesheets.HLine())

        ## Record Video Check Box
        self.programWidget_RecordVideo = QCheckBox("Record Video")
        self.programWidget_RecordVideo.setChecked(True)
        # Connect to recordVideo function
        self.programWidget_RecordVideo.stateChanged.connect(self.recordVideo)
        self.programWidget_DeviceParametersLayout.addWidget(self.programWidget_RecordVideo)

        ## Video Duration
        self.programWidget_VideoDurationLayout = QHBoxLayout()
        self.programWidget_DeviceParametersLayout.addLayout(self.programWidget_VideoDurationLayout)
        self.programWidget_VideoDurationLabel = QLabel("Video Duration (sec):")
        self.programWidget_VideoDurationLabel.setEnabled(True)
        self.programWidget_VideoDurationLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.programWidget_VideoDurationLayout.addWidget(self.programWidget_VideoDurationLabel)
        self.programWidget_VideoDuration = QDoubleSpinBox()
        self.programWidget_VideoDuration.setEnabled(True)
        self.programWidget_VideoDuration.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.programWidget_VideoDuration.setRange(1, 3600)
        self.programWidget_VideoDuration.setSingleStep(1)
        self.programWidget_VideoDuration.setDecimals(0)
        self.programWidget_VideoDuration.setValue(12)
        self.programWidget_VideoDurationLayout.addWidget(self.programWidget_VideoDuration)

        ## Video Directory
        self.programWidget_VideoDirectoryLayout = QHBoxLayout()
        self.programWidget_DeviceParametersLayout.addLayout(self.programWidget_VideoDirectoryLayout)
        self.programWidget_VideoDirectoryLabel = QLabel("Video Directory:")
        self.programWidget_VideoDirectoryLabel.setEnabled(True)
        self.programWidget_VideoDirectoryLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.programWidget_VideoDirectoryLayout.addWidget(self.programWidget_VideoDirectoryLabel)
        self.programWidget_VideoDirectoryButton = QPushButton("Change...")
        self.programWidget_VideoDirectoryButton.setEnabled(True)
        self.programWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))
        self.programWidget_VideoDirectoryButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # Connect to selectProgramVideoDirectory
        self.programWidget_VideoDirectoryButton.clicked.connect(self.selectProgramVideoDirectory)
        self.programWidget_VideoDirectoryLayout.addWidget(self.programWidget_VideoDirectoryButton)

        ## Horizontal separator
        self.programWidget_DeviceParametersLayout.addWidget(stylesheets.HLine())

    # Define buttons for program GUI
    def makeButtons(self):
        # Load Timings
        self.programWidget_LoadTimes = QPushButton("Load\nTimes")
        self.programWidget_LoadTimes.setFont(self.buttonFont)
        self.programWidget_LoadTimes.setFixedHeight(100)
        self.programWidget_LoadTimes.setFixedWidth(100)
        self.programWidget_LoadTimes.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.programWidget_LoadTimes.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.programWidget_LoadTimes.clicked.connect(self.loadTimes)
        self.programWidget_LoadingButtonsLayout.addWidget(self.programWidget_LoadTimes)

        # Load Locations
        self.programWidget_LoadLocations = QPushButton("Load\nLocations")
        self.programWidget_LoadLocations.setFont(self.buttonFont)
        self.programWidget_LoadLocations.setEnabled(False)
        self.programWidget_LoadLocations.setFixedHeight(100)
        self.programWidget_LoadLocations.setFixedWidth(100)
        self.programWidget_LoadLocations.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.programWidget_LoadLocations.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.programWidget_LoadLocations.clicked.connect(self.loadLocations)
        self.programWidget_LoadingButtonsLayout.addWidget(self.programWidget_LoadLocations)

        # Run Button
        self.programWidget_RunButton = QPushButton("Run")
        self.programWidget_RunButton.setFont(self.buttonFont)
        self.programWidget_RunButton.setEnabled(False)
        self.programWidget_RunButton.setFixedHeight(100)
        self.programWidget_RunButton.setFixedWidth(100)
        self.programWidget_RunButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.programWidget_RunButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.programWidget_RunButton.clicked.connect(self.runProgram)
        self.programWidget_OperatingButtonsLayout.addWidget(self.programWidget_RunButton)

        # Pause Button
        self.programWidget_PauseButton = QPushButton("Pause")
        self.programWidget_PauseButton.setFont(self.buttonFont)
        self.programWidget_PauseButton.setEnabled(False)
        self.programWidget_PauseButton.setFixedHeight(100)
        self.programWidget_PauseButton.setFixedWidth(100)
        self.programWidget_PauseButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.programWidget_PauseButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.programWidget_PauseButton.clicked.connect(self.pauseProgram)
        self.programWidget_OperatingButtonsLayout.addWidget(self.programWidget_PauseButton)

        # Stop Button
        self.programWidget_StopButton = QPushButton("Stop")
        self.programWidget_StopButton.setFont(self.buttonFont)
        self.programWidget_StopButton.setEnabled(False)
        self.programWidget_StopButton.setFixedHeight(100)
        self.programWidget_StopButton.setFixedWidth(100)
        self.programWidget_StopButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.programWidget_StopButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        self.programWidget_StopButton.clicked.connect(self.stopProgram)
        self.programWidget_OperatingButtonsLayout.addWidget(self.programWidget_StopButton)

    # Function to update gantry status
    def updateUseGantry(self):
        if self.programWidget_UseGantry.isChecked() is True:
            if (self.timesLoaded is True) and (self.locationsLoaded is True):
                self.programWidget_LoadLocations.setEnabled(True)
                self.programWidget_RunButton.setEnabled(True)
            elif (self.timesLoaded is True) and (self.locationsLoaded is False):
                self.programWidget_LoadLocations.setEnabled(True)
                self.programWidget_RunButton.setEnabled(False)
            else:
                self.programWidget_LoadLocations.setEnabled(False)
                self.programWidget_RunButton.setEnabled(False)
        elif self.programWidget_UseGantry.isChecked() is False:
            self.programWidget_LoadLocations.setEnabled(False)
            if (self.timesLoaded is True):
                self.programWidget_RunButton.setEnabled(True)
            else:
                self.programWidget_RunButton.setEnabled(False)

    # Function to update camera status
    def updateUseCamera(self):
        if (self.programWidget_UseCamera.isChecked() is True):
            self.programWidget_RecordVideo.setEnabled(True)
            if (self.programWidget_RecordVideo.isChecked() is True):
                self.programWidget_VideoDurationLabel.setEnabled(True)
                self.programWidget_VideoDuration.setEnabled(True)
                self.programWidget_VideoDirectoryLabel.setEnabled(True)
                self.programWidget_VideoDirectoryButton.setEnabled(True)
        elif (self.programWidget_UseCamera.isChecked() is False):
            self.programWidget_RecordVideo.setEnabled(False)
            self.programWidget_RecordVideo.setChecked(False)
            self.programWidget_VideoDurationLabel.setEnabled(False)
            self.programWidget_VideoDuration.setEnabled(False)
            self.programWidget_VideoDirectoryLabel.setEnabled(False)
            self.programWidget_VideoDirectoryButton.setEnabled(False)

    # Function to determine whether to record video
    def recordVideo(self):
        if (self.programWidget_RecordVideo.isChecked() is False):
            self.programWidget_VideoDurationLabel.setEnabled(False)
            self.programWidget_VideoDuration.setEnabled(False)
            self.programWidget_VideoDirectoryLabel.setEnabled(False)
            self.programWidget_VideoDirectoryButton.setEnabled(False)
        elif (self.programWidget_RecordVideo.isChecked() is True):
            self.programWidget_VideoDurationLabel.setEnabled(True)
            self.programWidget_VideoDuration.setEnabled(True)
            self.programWidget_VideoDirectoryLabel.setEnabled(True)
            self.programWidget_VideoDirectoryButton.setEnabled(True)
    
    # Function to set where to save outputs
    def selectProgramVideoDirectory(self):
        self.cameraOutputVideoDirectory = QFileDialog.getExistingDirectory(self, "Select folder directory where to save videos", "")
        if self.cameraOutputVideoDirectory != "":
            self.programWidget_VideoDirectoryButton.setToolTip(str(self.cameraOutputVideoDirectory))
        else:
            self.cameraOutputVideoDirectory = self.videoPath
            self.programWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))

    # Function to load times data froms csv
    def loadTimes(self):
        self.timesData = QFileDialog.getOpenFileName(self,'Select Times Document', "", "Text files (*.txt)")
        if (self.timesData[0] != ""):
            self.programWidget_LoadTimes.setToolTip(str(self.timesData[0]))
            self.timesDF = functions.getStartingTimes(self.timesData[0])
            self.timesLoaded = True
            if (self.programWidget_UseGantry.isChecked() is True):
                self.programWidget_LoadLocations.setEnabled(True)
                if (self.locationsLoaded is False):
                    self.programWidget_RunButton.setEnabled(False)
                elif (self.locationsLoaded is True):
                    self.programWidget_RunButton.setEnabled(True)
            elif (self.programWidget_UseGantry.isChecked() is False):
                self.programWidget_LoadLocations.setEnabled(False)
                self.programWidget_RunButton.setEnabled(True)
        else:
            self.programWidget_LoadTimes.setToolTip("")
            self.timesLoaded = False
            self.timesDF = None

    # Function to load locations data from csv
    def loadLocations(self):
        self.locationsData = QFileDialog.getOpenFileName(self,'Select Locations Document', "", "Text files (*.txt)")
        if (self.locationsData[0] != ""):
            self.programWidget_LoadLocations.setToolTip(str(self.locationsData[0]))
            self.moveCommands = functions.getMoveCommands(self.locationsData[0])
            self.locationsLoaded = True
            if (self.timesLoaded is True):
                self.programWidget_RunButton.setEnabled(True)
            else:
                self.programWidget_RunButton.setEnabled(False)
        else:
            self.programWidget_LoadLocations.setToolTip("")
            self.locationsLoaded = False
            self.moveCommands = None
            if (self.programWidget_UseGantry.isChecked() is True):
                self.programWidget_RunButton.setEnabled(False)
            else:
                self.programWidget_RunButton.setEnabled(True)

    # Function to launch program
    def runProgram(self):
        self.programThread = ProgramThread(
            self.programWidget_UseGantry.isChecked(),
            self.programWidget_UseCamera.isChecked(),
            self.timesDF,
            self.moveCommands,
            self.programWidget_RecordVideo.isChecked(),
            self.programWidget_VideoDuration.value(),
            self.cameraOutputVideoDirectory)
        self.programThread.programGantrySignal.connect(self.sendProgramGantrySignal)
        self.programThread.programCameraSignal.connect(self.sendProgramCameraSignal)
        self.programThread.start()

    # Function to pause program
    def pauseProgram(self):
        pass

    # Function to stop program
    def stopProgram(self):
        pass

    # Function to update gantry status
    def updateGantryConnectionStatus(self, signal):
        if (signal == 1):
            self.gantryConnected = True
        else:
            self.gantryConnected = False
        
        if (self.timesLoaded is True) and (self.locationsLoaded is True) and (self.gantryConnected is True) and (self.cameraConnected is True):
            self.programWidget_RunButton.setEnabled(True)
        else:
            self.programWidget_RunButton.setEnabled(False)

    # Function to update camera status
    def updateCameraConnectionStatus(self, signal):
        if (signal == 0) or (signal == 1):
            self.cameraConnected = False
        else:
            self.cameraConnected = True
        
        if (self.timesLoaded is True) and (self.locationsLoaded is True) and (self.gantryConnected is True) and (self.cameraConnected is True):
            self.programWidget_RunButton.setEnabled(True)
        else:
            self.programWidget_RunButton.setEnabled(False)
    
    # Send signals for gantry and camera
    def sendProgramGantrySignal(self, signal):
        self.programGantrySignal.emit(signal)

    def sendProgramCameraSignal(self, signal):
        self.programCameraSignal.emit(signal)
