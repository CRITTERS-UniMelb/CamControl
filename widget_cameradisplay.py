# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time

# Import local scripts


class CameraDisplayWidget(QGroupBox):

    # cameraDisplayDims = pyqtSignal(object)
    fullScreenSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.fullScreen = 0
        self.minimizedSizes = False
        self.maximizedSizes = False
        self.makeStylesheet()
        self.makeLayouts()
        self.makeButtons()
        self.makeDisplay()


    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white}
                """)


    def makeLayouts(self):
        # Main Layout
        self.cameraDisplay_MainLayout = QVBoxLayout(self)

        # Buttons Layout
        self.cameraDisplay_ButtonsLayout = QHBoxLayout()
        self.cameraDisplay_MainLayout.addLayout(self.cameraDisplay_ButtonsLayout, stretch=0)

        # Image Display Layout
        self.cameraDisplay_ImageDisplayLayout = QGridLayout()
        self.cameraDisplay_MainLayout.addLayout(self.cameraDisplay_ImageDisplayLayout, stretch=1)


    def makeButtons(self):
        self.cameraDisplayWidget_Fullscreen = QPushButton("Maximize Window")
        self.cameraDisplayWidget_Fullscreen.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cameraDisplayWidget_Fullscreen.clicked.connect(self.goFullScreen)
        self.cameraDisplay_ButtonsLayout.addWidget(self.cameraDisplayWidget_Fullscreen)

    
    def makeDisplay(self):
        # Camera Display
        # self.cameraWidget_CameraImageBG = QLabel()
        # self.cameraWidget_CameraImageBG.setPixmap(QPixmap())
        # self.cameraWidget_CameraImageBG.setText("Camera Disconnected")
        # self.cameraWidget_CameraImageBG.setAlignment(Qt.AlignCenter)
        # self.cameraWidget_CameraImageBG.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # self.cameraDisplay_ImageDisplayLayout.addWidget(self.cameraWidget_CameraImageBG, 0, 0, 1, 1)

        self.cameraWidget_CameraImage = QLabel()
        self.cameraWidget_CameraImage.setPixmap(QPixmap())
        self.cameraWidget_CameraImage.setAlignment(Qt.AlignCenter)
        self.cameraDisplay_ImageDisplayLayout.addWidget(self.cameraWidget_CameraImage, 0, 0, 1, 1)
    
    # def emitCameraDisplayDims(self, signal):
    #     if (signal == "Get Widget Dimensions"):
    #         self.cameraDisplayDims.emit([self.cameraWidget_CameraImageBG.width(), self.cameraWidget_CameraImageBG.height()])
    #         if self.minimizedSizes is False:
    #             self.minimizedWidth = self.cameraWidget_CameraImageBG.width()
    #             self.minimizedHeight = self.cameraWidget_CameraImageBG.height()
    #             self.minimizedSizes = True
    #     elif (signal == "Restore Widget Dimensions"):
    #         self.cameraDisplayDims.emit([self.minimizedWidth, self.minimizedHeight])
    
    def updateCameraDisplayImage(self, image):
        if (self.fullScreen == 0):
            imageScaled = image.scaled(self.imageMinimizedWidth, self.imageMinimizedHeight, Qt.KeepAspectRatio)
        elif (self.fullScreen == 1):
            imageScaled = image.scaled(self.cameraWidget_CameraImage.width(), self.cameraWidget_CameraImage.height(), Qt.KeepAspectRatio)
        img = imageScaled.mirrored(False,True)
        self.cameraWidget_CameraImage.setPixmap(QPixmap.fromImage(img))

    def calculateMinimizedGeometry(self):
        self.imageMinimizedWidth = self.cameraWidget_CameraImage.width()
        self.imageMinimizedHeight = self.cameraWidget_CameraImage.height()
        self.minimizedSizes = True

    def restoreMinimizedGeometry(self):
        self.cameraWidget_CameraImage.setFixedSize(self.imageMinimizedWidth, self.imageMinimizedHeight)

    def calculateMaximizedGeometry(self):
        if (self.maximizedSizes is False):
            self.imageMaximizedWidth = self.cameraWidget_CameraImage.width()
            self.imageMaximizedHeight = self.cameraWidget_CameraImage.height()
            self.maximizedSizes = True
    
    def restoreMaximizedGeometry(self):
        if (self.maximizedSizes is True):
            self.cameraWidget_CameraImage.setFixedSize(self.imageMaximizedWidth, self.imageMaximizedHeight)


    def showHideDisplayImage(self, status):
        if (status == 0):
            # self.cameraWidget_CameraImageBG.setText("Live Hidden")
            self.cameraWidget_CameraImage.hide()
        elif (status == 1):
            # self.cameraWidget_CameraImageBG.setText("Camera Connected")
            self.cameraWidget_CameraImage.show()


    def goFullScreen(self):
        if self.minimizedSizes is False:
            self.calculateMinimizedGeometry()

        if (self.fullScreen == 0):
            self.fullScreen = 1
            self.fullScreenSignal.emit(1)
            self.cameraDisplayWidget_Fullscreen.setText("Minimize Window")
        elif (self.fullScreen == 1):
            self.fullScreen = 0
            self.fullScreenSignal.emit(0)
            self.updateGeometry()
            self.cameraDisplayWidget_Fullscreen.setText("Maximize Window")