# Import packages
from ctypes import alignment
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime
import time
import os


# Import local scripts
from thread_camera import CameraThread
from thread_cameraTimer import CameraTimer
from thread_videoRecorder import VideoRecorder
import stylesheets

class CameraControlWidget(QGroupBox):

    # cameraInitialisation = pyqtSignal(object)
    cameraDisplayImage = pyqtSignal(object)
    cameraShowHideDisplay = pyqtSignal(int)
    cameraConnectionStatus = pyqtSignal(object)
    cameraCurrentAction = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.cameraSnapping = 0
        self.cameraRecording = 0
        self.cameraFrames = []
        self.savedVideoCounter = 1
        self.savedVideoNumber = "{0:04d}".format(self.savedVideoCounter)
        self.cameraConnected = 0
        self.makeStylesheet()
        self.makeLayouts()
        self.makeFonts()
        self.makeDirectories()
        self.makeInputs()
        self.makeButtons()
    
    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white}
                """)

    def makeLayouts(self):
        # Main Layout
        self.cameraWidgetLayout = QHBoxLayout(self)

        # Left Column Layout
        self.cameraWidgetLayout_LeftColumn = QVBoxLayout()
        self.cameraWidgetLayout_LeftColumn.setAlignment(Qt.AlignTop)
        self.cameraWidgetLayout.addLayout(self.cameraWidgetLayout_LeftColumn)

        # Add a vertical line separator between both columns
        self.cameraWidgetLayout.addWidget(stylesheets.VLine())

        # Right Column Layout
        self.cameraWidgetLayout_RightColumn = QVBoxLayout()
        self.cameraWidgetLayout_RightColumn.setAlignment(Qt.AlignTop)
        self.cameraWidgetLayout.addLayout(self.cameraWidgetLayout_RightColumn)

    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
        self.buttonFont = QFont("Sans Serif 10", 10)

    def makeDirectories(self):
        self.snapPath = os.path.join(os.path.dirname(__file__), 'snapshots')
        if not os.path.exists(self.snapPath):
            os.makedirs(self.snapPath)
        self.videoPath = os.path.join(os.path.dirname(__file__), 'videos')
        if not os.path.exists(self.videoPath):
            os.makedirs(self.videoPath)
        self.cameraOutputVideoDirectory = self.videoPath

    def makeInputs(self):
        # Title
        self.cameraWidget_Title = QLabel("Camera")
        self.cameraWidget_Title.setFont(QFont(self.futuraheavyfont_str, 16))
        self.cameraWidgetLayout_LeftColumn.addWidget(self.cameraWidget_Title, alignment=Qt.AlignCenter)

        # ComboBoxes Layout
        self.cameraWidgetParametersLayout = QGridLayout()
        self.cameraWidgetParametersLayout.setAlignment(Qt.AlignTop)
        self.cameraWidgetLayout_LeftColumn.addLayout(self.cameraWidgetParametersLayout)
        
        # Camera Selection
        self.cameraWidget_CameraSelectionLabel = QLabel("Camera Selection:")
        self.cameraWidget_CameraSelectionLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraSelectionLabel, 0, 0, 1, 1, alignment=Qt.AlignTop)
        self.cameraWidget_CameraSelection = QComboBox()
        self.cameraWidget_CameraSelection.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cameraWidget_CameraSelection.addItems(["CAM1 - XCAM4K8MPA - GXCAM HiChrome-HR4", "CAM2 - XCAM4K16MPA - GXCAM HiChrome-HR4 Hi Res", "CAM3 - XCAM4K16MPA - GXCAM HiChrome-HR4"])
        self.cameraWidget_CameraSelection.setCurrentIndex(1)
        self.cameraWidget_CameraSelection.currentIndexChanged.connect(self.cameraSelectionChanged)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraSelection, 0, 1, 1, 1, alignment=Qt.AlignTop)

        # Resolution Selection
        self.cameraWidget_CameraResolutionLabel = QLabel("Camera Resolution:")
        self.cameraWidget_CameraResolutionLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraResolutionLabel, 2, 0, 1, 1, alignment=Qt.AlignTop)
        self.cameraWidget_CameraResolution = QComboBox()
        self.cameraWidget_CameraResolution.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cameraWidget_CameraResolution.addItems(["5440x3060"])
        self.cameraWidget_CameraResolution.setCurrentIndex(0)
        self.cameraWidget_CameraResolution.currentIndexChanged.connect(self.cameraResolutionChanged)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_CameraResolution, 2, 1, 1, 1, alignment=Qt.AlignTop)

        # Video Directory
        self.cameraWidget_VideoDirectoryLabel = QLabel("Video Directory:")
        self.cameraWidget_VideoDirectoryLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoDirectoryLabel, 3, 0, 1, 1, alignment=Qt.AlignTop)
        self.cameraWidget_VideoDirectoryButton = QPushButton("Change...")
        self.cameraWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))
        self.cameraWidget_VideoDirectoryButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cameraWidget_VideoDirectoryButton.clicked.connect(self.selectCameraOutputVideoDirectory)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoDirectoryButton, 3, 1, 1, 1, alignment=Qt.AlignTop)

        # Video Name
        self.cameraWidget_VideoNameLabel = QLabel("Video Name:")
        self.cameraWidget_VideoNameLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoNameLabel, 4, 0, 1, 1, alignment=Qt.AlignTop)
        self.cameraWidget_VideoNameEntry = QLineEdit()
        self.cameraWidget_VideoNameEntry.setText(str(datetime.now().strftime("%Y-%m-%d")+"_"+"Video{}".format(self.savedVideoNumber)))
        self.cameraWidget_VideoNameEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoNameEntry, 4, 1, 1, 1, alignment=Qt.AlignTop)

        # Video Encoding
        self.cameraWidget_VideoEncodingLabel = QLabel("Video Encoding:")
        self.cameraWidget_VideoEncodingLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoEncodingLabel, 5, 0, 1, 1, alignment=Qt.AlignTop)
        self.cameraWidget_VideoEncoding = QComboBox()
        self.cameraWidget_VideoEncoding.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cameraWidget_VideoEncoding.addItems([".avi (MJPEG)", ".mp4 (H264)"])
        self.cameraWidget_VideoEncoding.setCurrentIndex(0)
        self.cameraWidget_VideoEncoding.currentIndexChanged.connect(self.cameraVideoEncodingChanged)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_VideoEncoding, 5, 1, 1, 1, alignment=Qt.AlignTop)

        # Auto-exposure
        self.cameraWidget_AutoExpo = QCheckBox("Auto Exposure")
        self.cameraWidget_AutoExpo.setChecked(True)
        self.cameraWidget_AutoExpo.stateChanged.connect(self.changeAutoExpo)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_AutoExpo, 6, 0, 1, 2)

        # Exposure Time
        self.cameraWidget_ExposureTimeLabel = QLabel()
        self.cameraWidget_ExposureTimeLabel.setText("Exposure Time (ms)")
        self.cameraWidget_ExposureTimeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraWidgetParametersLayout.addWidget(self.cameraWidget_ExposureTimeLabel, 7, 0, 1, 1, alignment=Qt.AlignTop)

        self.cameraWidget_ExposureTimeSelectorLayout = QHBoxLayout()
        self.cameraWidgetParametersLayout.addLayout(self.cameraWidget_ExposureTimeSelectorLayout, 7, 1, 1, 1, alignment=Qt.AlignTop)

        self.cameraWidget_ExposureTime = QSlider(Qt.Horizontal)
        self.cameraWidget_ExposureTime.setEnabled(False)
        self.cameraWidget_ExposureTime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cameraWidget_ExposureTime.setRange(0, 200)
        self.cameraWidget_ExposureTime.setFocusPolicy(Qt.NoFocus)
        self.cameraWidget_ExposureTime.setPageStep(1)
        self.cameraWidget_ExposureTime.setValue(33)
        self.cameraWidget_ExposureTime.valueChanged.connect(self.updateExposureTimeLabel)
        self.cameraWidget_ExposureTime.sliderReleased.connect(self.updateExposureTime)
        self.cameraWidget_ExposureTimeSelectorLayout.addWidget(self.cameraWidget_ExposureTime)

        self.cameraWidget_ExposureTimeSpin = QDoubleSpinBox()
        self.cameraWidget_ExposureTimeSpin.setEnabled(False)
        self.cameraWidget_ExposureTimeSpin.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraWidget_ExposureTimeSpin.setRange(0, 200)
        self.cameraWidget_ExposureTimeSpin.setSingleStep(1)
        self.cameraWidget_ExposureTimeSpin.setDecimals(0)
        self.cameraWidget_ExposureTimeSpin.setValue(33)
        self.cameraWidget_ExposureTimeSpin.valueChanged.connect(self.updateExposureTimeSpin)
        self.cameraWidget_ExposureTimeSelectorLayout.addWidget(self.cameraWidget_ExposureTimeSpin)

        
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
        self.cameraWidget_RecordButton.clicked.connect(self.recordMovie)
        self.cameraWidgetLayout_RightColumn.addWidget(self.cameraWidget_RecordButton)


    def connectCamera(self):
        if (self.cameraConnected == 0):
            # # Sending signal to get the size of the widget area where the camera image will be displayed
            # self.cameraInitialisation.emit("Get Widget Dimensions")

            # Creating the camera thread and its signal connections
            self.cameraThread = CameraThread()
            self.cameraThread.cameraNameSignal.connect(self.updateCameraConnection)
            self.cameraThread.cameraImage.connect(self.updateCameraDisplayImage)
            self.cameraThread.connectCamera()
        elif (self.cameraConnected == 1):
            self.cameraShowHideDisplay.emit(0)
            if self.cameraThread:
                self.cameraThread.stop()

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
            # Starting the camera thread to start the live streaming
            self.cameraThread.start()
            time.sleep(0.1)
            self.changeAutoExpo()
            if self.cameraWidget_AutoExpo.isChecked() is False:
                self.updateExposureTime()
            self.cameraCurrentAction.emit("Live Streaming")


    def snapPicture(self):
        self.cameraCurrentAction.emit("Capturing Screenshot")
        self.cameraSnapping = 1

    def recordMovie(self):
        if (self.cameraRecording == 0):
            self.cameraWidget_ConnectButton.setEnabled(False)
            self.cameraWidget_SnapButton.setEnabled(False)
            self.cameraWidget_RecordButton.setText("Stop")
            self.cameraRecording = 1
            self.cameraCurrentAction.emit("Recording Video")
            self.videoRecording_TimeInit = time.time()
        elif (self.cameraRecording == 1):
            self.cameraRecording = 0
            self.videoRecording_TimeFinal = time.time()
            self.cameraWidget_RecordButton.setText("Saving")
            self.cameraWidget_RecordButton.setEnabled(False)
            print("ELLY:    Total number of frames in the video is: {} ".format(len(self.cameraFrames)))
            self.makeVideo((self.cameraFrames, self.videoRecording_TimeInit, self.videoRecording_TimeFinal))
            self.cameraCurrentAction.emit("Saving Video")


    def cameraSelectionChanged(self):
        if (self.cameraWidget_CameraSelection.currentText() == "CAM1 - XCAM4K8MPA - GXCAM HiChrome-HR4"):
            self.cameraWidget_CameraResolution.clear()
            self.cameraWidget_CameraResolution.addItems(["3840x2160"])
            self.cameraWidget_CameraResolution.setCurrentIndex(0)
        elif (self.cameraWidget_CameraSelection.currentText() == "CAM2 - XCAM4K16MPA - GXCAM HiChrome-HR4 Hi Res"):
            self.cameraWidget_CameraResolution.clear()
            self.cameraWidget_CameraResolution.addItems(["5440x3060"])
            self.cameraWidget_CameraResolution.setCurrentIndex(0)
        elif (self.cameraWidget_CameraSelection.currentText() == "CAM3 - XCAM4K16MPA - GXCAM HiChrome-HR4"):
            self.cameraWidget_CameraResolution.clear()
            self.cameraWidget_CameraResolution.addItems(["5440x3060"])
            self.cameraWidget_CameraResolution.setCurrentIndex(0)


    def cameraResolutionChanged(self):
        pass

    def cameraVideoEncodingChanged(self):
        pass


    def changeAutoExpo(self):
        if (self.cameraConnected == 1):
            if self.cameraThread:
                self.cameraThread.changeAutoExposure(self.cameraWidget_AutoExpo.isChecked())

        if self.cameraWidget_AutoExpo.isChecked() is False:
            self.cameraWidget_ExposureTime.setEnabled(True)
            self.cameraWidget_ExposureTimeSpin.setEnabled(True)
        else:
            self.cameraWidget_ExposureTime.setValue(33)
            self.cameraWidget_ExposureTime.setEnabled(False)
            self.cameraWidget_ExposureTimeSpin.setEnabled(False)


    def updateExposureTime(self):
        if (self.cameraConnected == 1):
            if self.cameraThread:
                self.cameraThread.changeExposureTime(int(self.cameraWidget_ExposureTime.value()))
    
    def updateExposureTimeLabel(self):
        self.cameraWidget_ExposureTimeSpin.setValue(int(self.cameraWidget_ExposureTime.value()))
        self.updateExposureTime()

    def updateExposureTimeSpin(self):
        self.cameraWidget_ExposureTime.setValue(self.cameraWidget_ExposureTimeSpin.value())


    def selectCameraOutputVideoDirectory(self):
        self.cameraOutputVideoDirectory = QFileDialog.getExistingDirectory(self, "Select folder directory where to save videos", "")
        if self.cameraOutputVideoDirectory != "":
            self.cameraWidget_VideoDirectoryButton.setToolTip(str(self.cameraOutputVideoDirectory))
        else:
            self.cameraOutputVideoDirectory = self.videoPath
            self.cameraWidget_VideoDirectoryButton.setToolTip(str(self.videoPath))


    # def updateCameraDisplayDims(self, dims):
    #     self.cameraDisplayWidth = dims[0]
    #     self.cameraDisplayHeight = dims[1]


    def updateCameraDisplayImage(self, image):
        img = image.copy()
        if (self.cameraSnapping == 1):
            dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            snap = img.mirrored(False,True)
            snap.save("snapshots/{}.jpg".format(dt_string))
            self.cameraCurrentAction.emit("Screenshot Saved")
            self.cameraSnapping = 0
            self.cameraCurrentAction.emit("Live Streaming")
        if (self.cameraRecording == 1):
            # print("recording image {}".format(len(self.cameraFrames)))
            self.cameraFrames.append(img)

        self.cameraDisplayImage.emit(image)

    def makeVideo(self, videoPackage):
        encodingMethod = self.cameraWidget_VideoEncoding.currentIndex()
        if (encodingMethod == 1):
            videoName = str(self.cameraWidget_VideoNameEntry.text() + ".mp4")
        else:
            videoName = str(self.cameraWidget_VideoNameEntry.text() + ".avi")
        videoDirectory = str(self.cameraOutputVideoDirectory)
        videoPath = os.path.join(videoDirectory, videoName)
        self.videoRecorderThread = VideoRecorder(videoPackage, videoPath, encodingMethod)
        self.videoRecorderThread.currentAction.connect(self.updateRecorderAction)
        self.videoRecorderThread.start()
    
    def updateRecorderAction(self, action):
        if (action =="Video saved"):
            self.cameraCurrentAction.emit("Video Saved")
            self.savedVideoCounter += 1
            self.savedVideoNumber = "{0:04d}".format(self.savedVideoCounter)
            self.cameraWidget_VideoNameEntry.setText(str(datetime.now().strftime("%Y-%m-%d")+"_"+"Video{}".format(self.savedVideoNumber)))
            self.cameraWidget_ConnectButton.setEnabled(True)
            self.cameraWidget_RecordButton.setText("Record")
            self.cameraWidget_RecordButton.setEnabled(True)
            # Reinitializing the object storing the frames
            self.cameraFrames = []
            if self.cameraConnected == 1:
                self.cameraWidget_SnapButton.setEnabled(True)
                self.cameraWidget_RecordButton.setEnabled(True)
                self.cameraCurrentAction.emit("Live Streaming")
            else:
                self.cameraWidget_SnapButton.setEnabled(False)
                self.cameraWidget_RecordButton.setEnabled(False)
                self.cameraCurrentAction.emit("Disconnected")


    def programConnectCamera(self):
        if (self.cameraConnected == 0):
            self.connectCamera()
        else:
            pass
    
    def programDisconnectCamera(self):
        if (self.cameraConnected == 1):
            self.connectCamera()
        else:
            pass
    
    def programUpdateCameraParameters(self):
        # Updating the camera with exposure options
        if (self.cameraConnected == 1):
            if self.cameraThread:
                self.cameraThread.changeAutoExposure(self.cameraWidget_AutoExpo.isChecked())
            if self.cameraWidget_AutoExpo.isChecked() is False:
                if self.cameraThread:
                    self.cameraThread.changeExposureTime(int(self.cameraWidget_ExposureTime.value()))


    def programInitVideoRecord(self, signal):
        programVideoDuration = int(signal[1])
        self.cameraTimer = CameraTimer(programVideoDuration)
        self.cameraTimer.recordingSignal.connect(self.programAcquireVideoFrame)
        self.cameraTimer.initialization()
        self.cameraTimer.start()


    def programAcquireVideoFrame(self, signal):
        if signal is True:
            self.cameraRecording = 1
        if signal is False:
            self.cameraRecording = 0
    
    def programFinalizeVideoRecord(self, signal):
            print("ELLY:    Total number of frames in the video is: {} ".format(len(self.cameraFrames)))
            programVideoDuration = int(signal[1])
            if (self.cameraWidget_VideoEncoding.currentIndex() == 1):
                self.programVideoPath = str(signal[2])+".mp4"
            else:
                self.programVideoPath = str(signal[2])+".avi"
            programVideoPackage = [self.cameraFrames, 0, programVideoDuration]
            encodingMethod = self.cameraWidget_VideoEncoding.currentIndex()
            self.programVideoRecorderThread = VideoRecorder(programVideoPackage, self.programVideoPath, encodingMethod)
            self.programVideoRecorderThread.currentAction.connect(self.programVideoSaved)
            self.programVideoRecorderThread.start()

    def programVideoSaved(self, signal):
        if (signal == "Video saved"):
            print("ELLY:    Video {} saved".format(self.programVideoPath))
            # Reinitializing the object that stores the frame
            self.cameraFrames = []