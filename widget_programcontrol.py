# Import packages
from ctypes import alignment
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

# Import local scripts
from thread_program import ProgramThread
import functions
import stylesheets


class ProgramControlWidget(QGroupBox):

    programGantrySignal = pyqtSignal(object)
    programCameraSignal = pyqtSignal(object)

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

    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white}
                """)

    def makeLayouts(self):
        # Main Layout
        self.programWidget_Layout = QHBoxLayout(self)

        # Icon Layout
        self.programWidget_IconLayout = QVBoxLayout()
        self.programWidget_IconLayout.setAlignment(Qt.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_IconLayout)

        # Title and Device Selector Layout
        self.programWidget_TitleDeviceSelectorLayout = QVBoxLayout()
        self.programWidget_Layout.addLayout(self.programWidget_TitleDeviceSelectorLayout, stretch=1)

        # Title Layout
        self.programWidget_TitleLayout = QVBoxLayout()
        self.programWidget_TitleLayout.setAlignment(Qt.AlignTop)
        self.programWidget_TitleDeviceSelectorLayout.addLayout(self.programWidget_TitleLayout, stretch=0)

        # Device Selector Layout
        self.programWidget_DeviceSelectorLayout = QVBoxLayout()
        self.programWidget_DeviceSelectorLayout.setAlignment(Qt.AlignVCenter)
        self.programWidget_TitleDeviceSelectorLayout.addLayout(self.programWidget_DeviceSelectorLayout, stretch=1)

        # Vertical line separator 
        self.programWidget_Layout.addWidget(stylesheets.VLine())

        # Device Parameters Layout
        self.programWidget_DeviceParametersLayout = QVBoxLayout()
        self.programWidget_DeviceParametersLayout.setAlignment(Qt.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_DeviceParametersLayout, stretch=2)

        # Vertical line separator 
        self.programWidget_Layout.addWidget(stylesheets.VLine())

        # Loading Buttons Layout
        self.programWidget_LoadingButtonsLayout = QHBoxLayout()
        self.programWidget_LoadingButtonsLayout.setAlignment(Qt.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_LoadingButtonsLayout)

        # Vertical line separator 
        self.programWidget_Layout.addWidget(stylesheets.VLine())

        # Operating Buttons Layout
        self.programWidget_OperatingButtonsLayout = QHBoxLayout()
        self.programWidget_OperatingButtonsLayout.setAlignment(Qt.AlignVCenter)
        self.programWidget_Layout.addLayout(self.programWidget_OperatingButtonsLayout)


    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
        self.buttonFont = QFont("Sans Serif 10", 10)


    def makeDirectories(self):
        self.videoPath = os.path.join(os.path.dirname(__file__), 'videos')
        if not os.path.exists(self.videoPath):
            os.makedirs(self.videoPath)
        self.cameraOutputVideoDirectory = self.videoPath


    def makeIcon(self):
        self.programIcon = QLabel()
        programIconQPixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/icons/program.png'))
        self.programIcon.setPixmap(programIconQPixmap)
        self.programWidget_IconLayout.addWidget(self.programIcon)

    def makeTitle(self):
        # Title
        self.programWidget_Title = QLabel("Program")
        self.programWidget_Title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.programWidget_Title.setFont(QFont(self.futuraheavyfont_str, 16))
        self.programWidget_TitleLayout.addWidget(self.programWidget_Title, alignment=Qt.AlignCenter)


    def makeInputs(self):
        # Device selections
        self.programWidget_UseGantry = QCheckBox("Use Gantry")
        self.programWidget_UseGantry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.programWidget_UseGantry.setChecked(True)
        self.programWidget_UseGantry.stateChanged.connect(self.updateUseGantry)
        self.programWidget_DeviceSelectorLayout.addWidget(self.programWidget_UseGantry, alignment=Qt.AlignCenter)

        self.programWidget_UseCamera = QCheckBox("Use Camera")
        self.programWidget_UseCamera.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.programWidget_UseCamera.setChecked(True)
        self.programWidget_UseCamera.stateChanged.connect(self.updateUseCamera)
        self.programWidget_DeviceSelectorLayout.addWidget(self.programWidget_UseCamera, alignment=Qt.AlignCenter)

        # Device Parameters
        ## Horizontal separator
        self.programWidget_DeviceParametersLayout.addWidget(stylesheets.HLine())

        ## Record Video Check Box
        self.programWidget_RecordVideo = QCheckBox("Record Video")
        self.programWidget_RecordVideo.setChecked(True)
        self.programWidget_RecordVideo.stateChanged.connect(self.recordVideo)
        self.programWidget_DeviceParametersLayout.addWidget(self.programWidget_RecordVideo)

        ## Video Duration
        self.programWidget_VideoDurationLayout = QHBoxLayout()
        self.programWidget_DeviceParametersLayout.addLayout(self.programWidget_VideoDurationLayout)
        self.programWidget_VideoDurationLabel = QLabel("Video Duration (sec):")
        self.programWidget_VideoDurationLabel.setEnabled(True)
        self.programWidget_VideoDurationLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.programWidget_VideoDurationLayout.addWidget(self.programWidget_VideoDurationLabel)
        self.programWidget_VideoDuration = QDoubleSpinBox()
        self.programWidget_VideoDuration.setEnabled(True)
        self.programWidget_VideoDuration.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
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
        self.programWidget_VideoDirectoryLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.programWidget_VideoDirectoryLayout.addWidget(self.programWidget_VideoDirectoryLabel)
        self.programWidget_VideoDirectoryButton = QPushButton("Change...")
        self.programWidget_VideoDirectoryButton.setEnabled(True)
        self.programWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))
        self.programWidget_VideoDirectoryButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.programWidget_VideoDirectoryButton.clicked.connect(self.selectProgramVideoDirectory)
        self.programWidget_VideoDirectoryLayout.addWidget(self.programWidget_VideoDirectoryButton)

        ## Horizontal separator
        self.programWidget_DeviceParametersLayout.addWidget(stylesheets.HLine())


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
    
    def selectProgramVideoDirectory(self):
        self.cameraOutputVideoDirectory = QFileDialog.getExistingDirectory(self, "Select folder directory where to save videos", "")
        if self.cameraOutputVideoDirectory != "":
            self.programWidget_VideoDirectoryButton.setToolTip(str(self.cameraOutputVideoDirectory))
        else:
            self.cameraOutputVideoDirectory = self.videoPath
            self.programWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))

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

    def pauseProgram(self):
        pass

    def stopProgram(self):
        pass

    def updateGantryConnectionStatus(self, signal):
        if (signal == 1):
            self.gantryConnected = True
        else:
            self.gantryConnected = False
        
        if (self.timesLoaded is True) and (self.locationsLoaded is True) and (self.gantryConnected is True) and (self.cameraConnected is True):
            self.programWidget_RunButton.setEnabled(True)
        else:
            self.programWidget_RunButton.setEnabled(False)


    def updateCameraConnectionStatus(self, signal):
        if (signal == 0) or (signal == 1):
            self.cameraConnected = False
        else:
            self.cameraConnected = True
        
        if (self.timesLoaded is True) and (self.locationsLoaded is True) and (self.gantryConnected is True) and (self.cameraConnected is True):
            self.programWidget_RunButton.setEnabled(True)
        else:
            self.programWidget_RunButton.setEnabled(False)
    
    def sendProgramGantrySignal(self, signal):
        self.programGantrySignal.emit(signal)

    def sendProgramCameraSignal(self, signal):
        self.programCameraSignal.emit(signal)
