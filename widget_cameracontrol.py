# Import packages
import os
import time
from datetime import datetime

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Import local scripts
import stylesheets
from thread_camera import CameraThread
from thread_cameraTimer import CameraTimer
from thread_videoRecorder import VideoRecorder


# Set up camera control widget class
class CameraControlWidget(QGroupBox):
    
    # Set up signals for camera display image, display show/hide toggle,
    # connection status, and camera action
    cameraDisplayImage = pyqtSignal(object)
    cameraShowHideDisplay = pyqtSignal(int)
    cameraConnectionStatus = pyqtSignal(object)
    cameraCurrentAction = pyqtSignal(object)
    cameraExposure = pyqtSignal(int)

    # Set initiation commands
    def __init__(self):
        # Give access to parent methods
        super().__init__()
        # Set default for camera action indicators
        self.cameraSnapping = 0
        self.cameraRecording = 0
        # Set camera frames as empty 
        self.cameraFrames = []
        # Initialise video counter to 1
        self.savedVideoCounter = 1
        # Format video numbers 
        self.savedVideoNumber = f"{self.savedVideoCounter:04d}"
        # Set camera connection status to off
        self.cameraConnected = 0
        # Run syle functions
        self.makeStylesheet()
        self.makeLayouts()
        self.makeFonts()
        self.makeDirectories()
        self.makeInputs()
        self.makeButtons()
    
    # Define widget outline viduals
    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white}
                """)

    # Define camera control layout
    def makeLayouts(self):
        # Set main over-arching layout as a box
        self.cameraWidgetLayout = QHBoxLayout(self)

        # Add a left column to the main layout
        self.cameraWidgetLayout_LeftColumn = QVBoxLayout()
        self.cameraWidgetLayout_LeftColumn.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cameraWidgetLayout.addLayout(self.cameraWidgetLayout_LeftColumn)

        # Add a vertical line separator between both columns
        self.cameraWidgetLayout.addWidget(stylesheets.VLine())

        # Add a right column to the main layout
        self.cameraWidgetLayout_RightColumn = QVBoxLayout()
        self.cameraWidgetLayout_RightColumn.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cameraWidgetLayout.addLayout(self.cameraWidgetLayout_RightColumn)

    # Method for setting application fonts
    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        futuralightfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Light font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
        self.futuralightfont_str = QFontDatabase.applicationFontFamilies(futuralightfont)[0]
        self.buttonFont = QFont(self.futuralightfont_str, 10)

    # Method to create paths for snapshots & videos (if not already existing)
    def makeDirectories(self):
        self.snapPath = os.path.join(os.path.dirname(__file__), 'snapshots')
        if not os.path.exists(self.snapPath):
            os.makedirs(self.snapPath)
        self.videoPath = os.path.join(os.path.dirname(__file__), 'videos')
        if not os.path.exists(self.videoPath):
            os.makedirs(self.videoPath)
        # Set default output directory to the automatically created video path
        self.cameraOutputVideoDirectory = self.videoPath

    # Method for defining the camera control inputs
    def makeInputs(self):
        # Title
        # Create title box and add to left column of parent inputs layout
        self.cameraWidget_Title = QLabel("Camera")
        self.cameraWidget_Title.setFont(QFont(self.futuraheavyfont_str, 16))
        self.cameraWidgetLayout_LeftColumn.addWidget(self.cameraWidget_Title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create box for parameters
        self.cameraWidgetParametersLayout = QGridLayout()
        self.cameraWidgetParametersLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Add to left column of parent inputs layout
        self.cameraWidgetLayout_LeftColumn.addLayout(self.cameraWidgetParametersLayout)
        
        # Camera Selection
        # Create camera selection label and set size, add to parameter layout
        self.cameraWidget_CameraSelectionLabel = QLabel("Camera Selection:")
        self.cameraWidget_CameraSelectionLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraSelectionLabel, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # Create drop-down box for camera selection
        self.cameraWidget_CameraSelection = QComboBox()
        self.cameraWidget_CameraSelection.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # Define camera options
        self.cameraWidget_CameraSelection.addItems(["CAM1 - XCAM4K8MPA - GXCAM HiChrome-HR4", "CAM2 - XCAM4K16MPA - GXCAM HiChrome-HR4 Hi Res", "CAM3 - XCAM4K16MPA - GXCAM HiChrome-HR4"])
        # Set camera default to 2nd option
        self.cameraWidget_CameraSelection.setCurrentIndex(1)
        # Connect to function for changing camera
        self.cameraWidget_CameraSelection.currentIndexChanged.connect(self.cameraSelectionChanged)
        # Add to parameters layout
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraSelection, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)

        # Resolution Selection
        # Create camera selection label and set size, add to parameter layout
        self.cameraWidget_CameraResolutionLabel = QLabel("Camera Resolution:")
        self.cameraWidget_CameraResolutionLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraResolutionLabel, 2, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # Create drop-down menu for resolution
        self.cameraWidget_CameraResolution = QComboBox()
        self.cameraWidget_CameraResolution.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # Define resolution options
        self.cameraWidget_CameraResolution.addItems(["5440x3060"])
        # Set default option
        self.cameraWidget_CameraResolution.setCurrentIndex(0)
        # Connect to function for changing resolution
        self.cameraWidget_CameraResolution.currentIndexChanged.connect(self.cameraResolutionChanged)
        # Add to parameters layout
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraResolution, 2, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)

        # Video Directory
        # Create vid directory label and set size, add to parameter layout
        self.cameraWidget_VideoDirectoryLabel = QLabel("Video Directory:")
        self.cameraWidget_VideoDirectoryLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoDirectoryLabel, 3, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # Add push-button for choosing directory
        self.cameraWidget_VideoDirectoryButton = QPushButton("Change...")
        self.cameraWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))
        self.cameraWidget_VideoDirectoryButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # Connect push-button to output selector function
        self.cameraWidget_VideoDirectoryButton.clicked.connect(self.selectCameraOutputVideoDirectory)
        # Add to parameters layout
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoDirectoryButton, 3, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)

        # Video Name
        # Create vid name label and set size, add to parameter layout
        self.cameraWidget_VideoNameLabel = QLabel("Video Name:")
        self.cameraWidget_VideoNameLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoNameLabel, 4, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # Create editable line input
        self.cameraWidget_VideoNameEntry = QLineEdit()
        # Set default to current date and video number
        self.cameraWidget_VideoNameEntry.setText(str(datetime.now().astimezone().strftime("%Y-%m-%d")+"_"+f"Video{self.savedVideoNumber}"))
        self.cameraWidget_VideoNameEntry.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # Add to parameters layout
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoNameEntry, 4, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)

        # Video Encoding
        # Create video encoding label, set size, and add to parameter layout
        self.cameraWidget_VideoEncodingLabel = QLabel("Video Encoding:")
        self.cameraWidget_VideoEncodingLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoEncodingLabel, 5, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # Create drop-down menu
        self.cameraWidget_VideoEncoding = QComboBox()
        self.cameraWidget_VideoEncoding.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.cameraWidget_VideoEncoding.addItems([".avi (MJPEG)", ".mp4 (H264)"])
        # Set default to AVI
        self.cameraWidget_VideoEncoding.setCurrentIndex(0)
        # Connect to function to update video encoding
        self.cameraWidget_VideoEncoding.currentIndexChanged.connect(self.cameraVideoEncodingChanged)
        # Add to parameters layout
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoEncoding, 5, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)



        # Exposure Time
        # Create exposure time label and add to parameter layout
        self.cameraWidget_ExposureTimeLabel = QLabel()
        self.cameraWidget_ExposureTimeLabel.setText("Exposure Time (ms)")
        self.cameraWidget_ExposureTimeLabel.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_ExposureTimeLabel, 7, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # Add exposure time box
        self.cameraWidget_ExposureTimeSelectorLayout = QHBoxLayout()
        self.cameraWidgetParametersLayout.addLayout(self.cameraWidget_ExposureTimeSelectorLayout, 7, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignTop)
        # Add slider for exposure time
        self.cameraWidget_ExposureTime = QSlider(Qt.Orientation.Horizontal)
        self.cameraWidget_ExposureTime.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # Set possible range from 0 to 200
        self.cameraWidget_ExposureTime.setRange(0, 200)
        self.cameraWidget_ExposureTime.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cameraWidget_ExposureTime.setPageStep(1)
        # Set initial value to 33
        self.cameraWidget_ExposureTime.setValue(33)
        # Connect to functions for updating exposure time
        self.cameraWidget_ExposureTime.valueChanged.connect(self.updateExposureTimeLabel)
        self.cameraWidget_ExposureTime.sliderReleased.connect(self.updateExposureTime)
        # Add to parameters layout
        self.cameraWidget_ExposureTimeSelectorLayout.addWidget(self.cameraWidget_ExposureTime)

        # Add alternate entry box for exposure time
        self.cameraWidget_ExposureTimeSpin = QDoubleSpinBox()
        self.cameraWidget_ExposureTimeSpin.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # Set possible range and default
        self.cameraWidget_ExposureTimeSpin.setRange(0, 200)
        self.cameraWidget_ExposureTimeSpin.setSingleStep(1)
        self.cameraWidget_ExposureTimeSpin.setDecimals(0)
        self.cameraWidget_ExposureTimeSpin.setValue(33)
        # Connect to exposure time change functions
        self.cameraWidget_ExposureTimeSpin.valueChanged.connect(self.updateExposureTimeSpin)
        self.cameraWidget_ExposureTimeSelectorLayout.addWidget(self.cameraWidget_ExposureTimeSpin)

    # Method to define the buttons for camera controls
    def makeButtons(self):
        # Icon
        self.cameraIcon = QLabel()
        cameraIconQPixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/icons/camera.png'))
        self.cameraIcon.setPixmap(cameraIconQPixmap)
        self.cameraWidgetLayout_RightColumn.addWidget(self.cameraIcon)

        # Connect/Disconnect Camera Button
        self.cameraWidget_ConnectButton = QPushButton("Connect")
        self.cameraWidget_ConnectButton.setFont(self.buttonFont)
        self.cameraWidget_ConnectButton.setFixedHeight(100)
        self.cameraWidget_ConnectButton.setFixedWidth(100)
        self.cameraWidget_ConnectButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.cameraWidget_ConnectButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        # When clicked, run connectCamera function
        self.cameraWidget_ConnectButton.clicked.connect(self.connectCamera)
        self.cameraWidgetLayout_RightColumn.addWidget(self.cameraWidget_ConnectButton)

        # Snap Button
        self.cameraWidget_SnapButton = QPushButton("Snap")
        self.cameraWidget_SnapButton.setFont(self.buttonFont)
        self.cameraWidget_SnapButton.setEnabled(False)
        self.cameraWidget_SnapButton.setFixedHeight(100)
        self.cameraWidget_SnapButton.setFixedWidth(100)
        self.cameraWidget_SnapButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.cameraWidget_SnapButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        # When clicked, run snapPicture function
        self.cameraWidget_SnapButton.clicked.connect(self.snapPicture)
        self.cameraWidgetLayout_RightColumn.addWidget(self.cameraWidget_SnapButton)

        # Record Button
        self.cameraWidget_RecordButton = QPushButton("Record")
        self.cameraWidget_RecordButton.setFont(self.buttonFont)
        self.cameraWidget_RecordButton.setEnabled(False)
        self.cameraWidget_RecordButton.setFixedHeight(100)
        self.cameraWidget_RecordButton.setFixedWidth(100)
        self.cameraWidget_RecordButton.setStyleSheet(stylesheets.getQPushButtonStyle1(50))
        self.cameraWidget_RecordButton.setGraphicsEffect(stylesheets.getQPushButtonStyle1_shadow())
        # When clicked, run recordMovie function
        self.cameraWidget_RecordButton.clicked.connect(self.recordMovie)
        self.cameraWidgetLayout_RightColumn.addWidget(self.cameraWidget_RecordButton)

    # Define function to connect camera
    def connectCamera(self):
        # If not connected, create thread
        if (self.cameraConnected == 0):
            # Create the camera thread and its signal connections
            self.cameraThread = CameraThread()
            self.cameraThread.cameraNameSignal.connect(self.updateCameraConnection)
            self.cameraThread.cameraImage.connect(self.updateCameraDisplayImage)
            self.cameraExposure.connect(self.cameraThread.changeExposureTime)
            # Starting the camera thread to start the live streaming
            self.cameraThread.start()
        # If already connected, disconnect when function is run
        elif (self.cameraConnected == 1):
            self.cameraShowHideDisplay.emit(0)
            if self.cameraThread:
                self.cameraThread.stop()

    # Define function to update camera connection signal
    def updateCameraConnection(self, cameraName):
        if cameraName is None:
            self.cameraConnected = 0
            self.cameraShowHideDisplay.emit(0)
            self.cameraWidget_ConnectButton.setText("Connect")
            self.cameraWidget_SnapButton.setEnabled(False)
            self.cameraWidget_RecordButton.setEnabled(False)
            self.cameraConnectionStatus.emit(1)  # Status 1 means "failed to connect"
            self.cameraCurrentAction.emit("Disconnected")
        elif cameraName == 0:
            self.cameraConnected = 0
            self.cameraShowHideDisplay.emit(0)
            self.cameraWidget_ConnectButton.setText("Connect")
            self.cameraWidget_SnapButton.setEnabled(False)
            self.cameraWidget_RecordButton.setEnabled(False)
            self.cameraConnectionStatus.emit(0)  # Status 0 means "Disconnected"
            self.cameraCurrentAction.emit("Disconnected")
        else:
            self.cameraConnected = 1
            self.cameraShowHideDisplay.emit(1)
            self.cameraWidget_ConnectButton.setText("Disconnect")
            self.cameraConnectionStatus.emit(cameraName)
            # Enabling the options to snap and record the live stream
            self.cameraWidget_SnapButton.setEnabled(True)
            self.cameraWidget_RecordButton.setEnabled(True)
            time.sleep(0.1)
            self.updateExposureTime()
            self.cameraCurrentAction.emit("Live Streaming")

    # Define function for snapping picture
    def snapPicture(self):
        self.cameraCurrentAction.emit("Capturing Screenshot")
        self.cameraSnapping = 1

    # Define function for recording video
    def recordMovie(self):
        # On first run, start recording 
        if (self.cameraRecording == 0):
            self.cameraWidget_ConnectButton.setEnabled(False)
            self.cameraWidget_SnapButton.setEnabled(False)
            self.cameraWidget_RecordButton.setText("Stop")
            self.cameraRecording = 1
            self.cameraCurrentAction.emit("Recording Video")
            self.videoRecording_TimeInit = time.time()
        # On second run,  stop recording
        elif (self.cameraRecording == 1):
            self.cameraRecording = 0
            self.videoRecording_TimeFinal = time.time()
            self.cameraWidget_RecordButton.setText("Saving")
            self.cameraWidget_RecordButton.setEnabled(False)
            print(f"ELLY:    Total number of frames in the video is: {len(self.cameraFrames)}")
            # Run make video function
            self.makeVideo((self.cameraFrames, self.videoRecording_TimeInit, self.videoRecording_TimeFinal))
            self.cameraCurrentAction.emit("Saving Video")

    # Define function for changing camera
    def cameraSelectionChanged(self):
        if (self.cameraWidget_CameraSelection.currentText() == "CAM1 - XCAM4K8MPA - GXCAM HiChrome-HR4"):
            self.cameraWidget_CameraResolution.clear()
            self.cameraWidget_CameraResolution.addItems(["3840x2160"])
            self.cameraWidget_CameraResolution.setCurrentIndex(0)
        elif (self.cameraWidget_CameraSelection.currentText() == "CAM2 - XCAM4K16MPA - GXCAM HiChrome-HR4 Hi Res") or (self.cameraWidget_CameraSelection.currentText() == "CAM3 - XCAM4K16MPA - GXCAM HiChrome-HR4"):
            self.cameraWidget_CameraResolution.clear()
            self.cameraWidget_CameraResolution.addItems(["5440x3060"])
            self.cameraWidget_CameraResolution.setCurrentIndex(0)
        elif (self.cameraWidget_CameraSelection.currentText() == "Tucsen MIchrome 20"):
            self.cameraWidget_CameraResolution.clear()
            self.cameraWidget_CameraResolution.addItems(["5472x3648"])
            self.cameraWidget_CameraResolution.setCurrentIndex(0)

    # Empty methods for changing resolution and encoding
    def cameraResolutionChanged(self):
        pass

    def cameraVideoEncodingChanged(self):
        pass



    # Define method for changing exposure time
    def updateExposureTime(self):
        self.cameraExposure.emit(int(self.cameraWidget_ExposureTime.value()))
    
    # Define method for changing exposure time
    def updateExposureTimeLabel(self):
        self.cameraWidget_ExposureTimeSpin.setValue(int(self.cameraWidget_ExposureTime.value()))

    # Update spin selector for exposure time
    def updateExposureTimeSpin(self):
        self.cameraWidget_ExposureTime.setValue(int(self.cameraWidget_ExposureTimeSpin.value()))

    #  Function to update video output directory
    def selectCameraOutputVideoDirectory(self):
        self.cameraOutputVideoDirectory = QFileDialog.getExistingDirectory(self, "Select folder directory where to save videos", "")
        # If already has one - set tooltip to directory.
        if self.cameraOutputVideoDirectory != "":
            self.cameraWidget_VideoDirectoryButton.setToolTip(str(self.cameraOutputVideoDirectory))
        # If doesn't have one - set to self.videopath
        else:
            self.cameraOutputVideoDirectory = self.videoPath
            self.cameraWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))

    # Function to update the camera image displayed
    def updateCameraDisplayImage(self, image):
        img = image.copy()
        # If snapping images:
        if (self.cameraSnapping == 1):
            dt_string = datetime.now().astimezone().strftime("%Y-%m-%d-%H-%M-%S")
            # Flip image
            snap = img.mirrored(False,True)
            # Save with dateime
            snap.save(f"snapshots/{dt_string}.jpg" "snapshots/{}.jpg")
            self.cameraCurrentAction.emit("Screenshot Saved")
            self.cameraSnapping = 0
            self.cameraCurrentAction.emit("Live Streaming")
        # If actively recording:
        if (self.cameraRecording == 1):
            # Add image to camera frames
            self.cameraFrames.append(img)
        # Show camera image
        self.cameraDisplayImage.emit(image)

    # Function to launch video recording thread
    def makeVideo(self, videoPackage):
        # Set encoding method
        encodingMethod = self.cameraWidget_VideoEncoding.currentIndex()
        # Save as either MP4 or AVI
        if (encodingMethod == 1):
            videoName = str(self.cameraWidget_VideoNameEntry.text() + ".mp4")
        else:
            videoName = str(self.cameraWidget_VideoNameEntry.text() + ".avi")
        # Create full filepath
        videoDirectory = str(self.cameraOutputVideoDirectory)
        videoPath = os.path.join(videoDirectory, videoName)
        # Create thread with video recorder function
        self.videoRecorderThread = VideoRecorder(videoPackage, videoPath, encodingMethod)
        # Allow thread to connect with recorder action
        self.videoRecorderThread.currentAction.connect(self.updateRecorderAction)
        # Start thread
        self.videoRecorderThread.start()
    
    # Once video is saved, add to counter and reset camera frames
    def updateRecorderAction(self, action):
        if (action =="Video saved"):
            self.cameraCurrentAction.emit("Video Saved")
            self.savedVideoCounter += 1
            self.savedVideoNumber = f"{self.savedVideoCounter:04d}"
            self.cameraWidget_VideoNameEntry.setText(str(datetime.now().astimezone().strftime("%Y-%m-%d")+"_"+f"Video{self.savedVideoNumber}"))
            self.cameraWidget_ConnectButton.setEnabled(True)
            self.cameraWidget_RecordButton.setText("Record")
            self.cameraWidget_RecordButton.setEnabled(True)
            # Reinitializing the object storing the frames
            self.cameraFrames = []
            # If camera still connected, resume live streaming
            if self.cameraConnected == 1:
                self.cameraWidget_SnapButton.setEnabled(True)
                self.cameraWidget_RecordButton.setEnabled(True)
                self.cameraCurrentAction.emit("Live Streaming")
            else:
                self.cameraWidget_SnapButton.setEnabled(False)
                self.cameraWidget_RecordButton.setEnabled(False)
                self.cameraCurrentAction.emit("Disconnected")

    # Function for connecting camera as part of program
    def programConnectCamera(self):
        if (self.cameraConnected == 0):
            self.connectCamera()
        else:
            pass
    
    # Function for disconnecting camera as part of program
    def programDisconnectCamera(self):
        if (self.cameraConnected == 1):
            self.connectCamera()
        else:
            pass
    
    # Function for updating camera parameters as part of a program
    def programUpdateCameraParameters(self):
        # Updating the camera with exposure options
        if (self.cameraConnected == 1) and (self.cameraThread):
            self.cameraThread.changeExposureTime(int(self.cameraWidget_ExposureTime.value()))

    # Begin recording video as part of a program
    def programInitVideoRecord(self, signal):
        programVideoDuration = int(signal[1])
        # Begin timer for video reocrding
        self.cameraTimer = CameraTimer(programVideoDuration)
        # Connect to video frame acquire function
        self.cameraTimer.recordingSignal.connect(self.programAcquireVideoFrame)
        # Initialise timer
        self.cameraTimer.initialization()
        self.cameraTimer.start()

    # While program is running, determines when to record video
    def programAcquireVideoFrame(self, signal):
        if signal is True:
            self.cameraRecording = 1
        if signal is False:
            self.cameraRecording = 0
    
    # Function to finish recording as part of a program
    def programFinalizeVideoRecord(self, signal):
            print(f"ELLY:    Total number of frames in the video is: {len(self.cameraFrames)} ")
            programVideoDuration = int(signal[1])
            if (self.cameraWidget_VideoEncoding.currentIndex() == 1):
                self.programVideoPath = str(signal[2])+".mp4"
            else:
                self.programVideoPath = str(signal[2])+".avi"
            programVideoPackage = [self.cameraFrames, 0, programVideoDuration]
            encodingMethod = self.cameraWidget_VideoEncoding.currentIndex()
            # Start video reocrder thread
            self.programVideoRecorderThread = VideoRecorder(programVideoPackage, self.programVideoPath, encodingMethod)
            self.programVideoRecorderThread.currentAction.connect(self.programVideoSaved)
            self.programVideoRecorderThread.start()

    # Function to declare that a video was saved as part of program
    def programVideoSaved(self, signal):
        if (signal == "Video saved"):
            print(f"ELLY:    Video {self.programVideoPath} saved")
            # Reinitializing the object that stores the frame
            self.cameraFrames = []