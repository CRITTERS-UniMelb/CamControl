# Import packages
from ctypes import alignment
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

# Import local scripts
import stylesheets

class StatusWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.cameraConnected = 0
        self.cameraDisplayed = 0

        self.makeStylesheet()
        self.makeLayouts()
        self.makeFonts()
        self.makeIcon()
        self.makeTitle()
        self.makeConnectionLabels()

    def makeStylesheet(self):
        self.setStyleSheet("""
                QGroupBox{border: 1px solid black; border-radius: 5px; background-color:white;}
                """)
    
    def makeLayouts(self):
        # Main Layout
        self.statusWidget_MainLayout = QHBoxLayout(self)

        # Icon Layout (left column)
        self.statusWidget_IconLayout = QVBoxLayout()
        self.statusWidget_IconLayout.setAlignment(Qt.AlignVCenter)
        self.statusWidget_MainLayout.addLayout(self.statusWidget_IconLayout, stretch=0)

        # Information layout (right column)
        self.statusWidget_InformationLayout = QVBoxLayout()
        self.statusWidget_MainLayout.addLayout(self.statusWidget_InformationLayout, stretch=1)

        # Title Layout
        self.statusWidgetTitleRow = QVBoxLayout()
        self.statusWidgetTitleRow.setAlignment(Qt.AlignTop|Qt.AlignCenter)
        self.statusWidget_InformationLayout.addLayout(self.statusWidgetTitleRow, stretch=0)

        # Connection Status Overall Layout
        self.statusWidgetStatusRow = QHBoxLayout()
        self.statusWidgetStatusRow.setAlignment(Qt.AlignVCenter)
        self.statusWidget_InformationLayout.addLayout(self.statusWidgetStatusRow, stretch=1)

        # Connection Status Left Column Layout
        self.statusWidgetLayout_LeftColumn = QVBoxLayout()
        self.statusWidgetLayout_LeftColumn.setAlignment(Qt.AlignCenter)
        self.statusWidgetStatusRow.addLayout(self.statusWidgetLayout_LeftColumn)

        # Gantry Connection Status Layout
        self.statusWidget_GantryConnectionStatusLayout = QHBoxLayout()
        self.statusWidgetLayout_LeftColumn.addLayout(self.statusWidget_GantryConnectionStatusLayout)

        # Gantry Current Action Layout
        self.statusWidget_GantryActionStatusLayout = QHBoxLayout()
        self.statusWidgetLayout_LeftColumn.addLayout(self.statusWidget_GantryActionStatusLayout)

        # Gantry Current Location Layout
        self.statusWidget_GantryCoordsLayout = QHBoxLayout()
        self.statusWidgetLayout_LeftColumn.addLayout(self.statusWidget_GantryCoordsLayout)

        # Add a vertical line separator between both columns
        self.statusWidgetStatusRow.addWidget(stylesheets.VLine())

        # Connection Status Right Column Layout
        self.statusWidgetLayout_RightColumn = QVBoxLayout()
        self.statusWidgetLayout_RightColumn.setAlignment(Qt.AlignCenter)
        self.statusWidgetStatusRow.addLayout(self.statusWidgetLayout_RightColumn)

        # Camera Connection Status Layout
        self.statusWidget_CameraConnectionStatusLayout = QHBoxLayout()
        self.statusWidgetLayout_RightColumn.addLayout(self.statusWidget_CameraConnectionStatusLayout)

        # Camera Action Status Layout
        self.statusWidget_cameraActionStatusLayout = QHBoxLayout()
        self.statusWidgetLayout_RightColumn.addLayout(self.statusWidget_cameraActionStatusLayout)

        # Horizontal separator in right column
        self.statusWidgetLayout_RightColumn.addWidget(stylesheets.HLine())

    def makeFonts(self):
        futuraheavyfont = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'font/Futura/Futura Heavy font.ttf'))
        self.futuraheavyfont_str = QFontDatabase.applicationFontFamilies(futuraheavyfont)[0]
    
    def makeIcon(self):
        # Icon
        self.informationIcon = QLabel()
        informationIconQPixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/icons/connection.png'))
        self.informationIcon.setPixmap(informationIconQPixmap)
        self.statusWidget_IconLayout.addWidget(self.informationIcon)

    def makeTitle(self):
        # Title
        self.statusWidget_Title = QLabel("Information")
        self.statusWidget_Title.setFont(QFont(self.futuraheavyfont_str, 16))
        self.statusWidgetTitleRow.addWidget(self.statusWidget_Title, alignment=Qt.AlignTop|Qt.AlignCenter)

    def makeConnectionLabels(self):
        # Gantry Connection Status
        self.statusWidget_GantryConnectionStatusLabel = QLabel("Gantry connection status:")
        self.statusWidget_GantryConnectionStatusLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.statusWidget_GantryConnectionStatusLayout.addWidget(self.statusWidget_GantryConnectionStatusLabel, alignment=Qt.AlignCenter)

        self.statusWidget_GantryConnectionStatus = QLabel("Disconnected")
        self.statusWidget_GantryConnectionStatus.setStyleSheet("color: red;")
        self.statusWidget_GantryConnectionStatus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.statusWidget_GantryConnectionStatusLayout.addWidget(self.statusWidget_GantryConnectionStatus, alignment=Qt.AlignCenter)

        # Gantry Current Action
        self.statusWidget_GantryActionStatusLabel = QLabel("Gantry current action:")
        self.statusWidget_GantryActionStatusLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.statusWidget_GantryActionStatusLayout.addWidget(self.statusWidget_GantryActionStatusLabel, alignment=Qt.AlignCenter)

        self.statusWidget_GantryActionStatus = QLabel("Disconnected")
        self.statusWidget_GantryActionStatus.setStyleSheet("color: red;")
        self.statusWidget_GantryActionStatus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.statusWidget_GantryActionStatusLayout.addWidget(self.statusWidget_GantryActionStatus, alignment=Qt.AlignCenter)

        # Gantry Current Location
        self.statusWidget_GantryCoordsLabel = QLabel("Gantry current coordinates:")
        self.statusWidget_GantryCoordsLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.statusWidget_GantryCoordsLayout.addWidget(self.statusWidget_GantryCoordsLabel, alignment=Qt.AlignCenter)

        self.statusWidget_GantryCoords = QLabel("NA")
        self.statusWidget_GantryCoords.setStyleSheet("color: red;")
        self.statusWidget_GantryCoords.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.statusWidget_GantryCoordsLayout.addWidget(self.statusWidget_GantryCoords, alignment=Qt.AlignCenter)

        # Camera Connection Status
        self.statusWidget_CameraConnectionStatusLabel = QLabel("Camera connection status:")
        self.statusWidget_CameraConnectionStatusLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.statusWidget_CameraConnectionStatusLayout.addWidget(self.statusWidget_CameraConnectionStatusLabel, alignment=Qt.AlignCenter)

        self.statusWidget_CameraConnectionStatus = QLabel("Disconnected")
        self.statusWidget_CameraConnectionStatus.setStyleSheet("color: red;")
        self.statusWidget_CameraConnectionStatus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.statusWidget_CameraConnectionStatusLayout.addWidget(self.statusWidget_CameraConnectionStatus, alignment=Qt.AlignCenter)

        # Camera Action Status
        self.statusWidget_cameraActionStatusLabel = QLabel("Camera current action:")
        self.statusWidget_cameraActionStatusLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.statusWidget_cameraActionStatusLayout.addWidget(self.statusWidget_cameraActionStatusLabel, alignment=Qt.AlignCenter)

        self.statusWidget_cameraActionStatus = QLabel("Disconnected")
        self.statusWidget_cameraActionStatus.setStyleSheet("color: red;")
        self.statusWidget_cameraActionStatus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.statusWidget_cameraActionStatusLayout.addWidget(self.statusWidget_cameraActionStatus, alignment=Qt.AlignCenter)


    def updateGantryConnectionStatus(self, status):
        if (status == 0):
            self.statusWidget_GantryConnectionStatus.setText("Disconnected")
            self.statusWidget_GantryConnectionStatus.setStyleSheet("color: red;")
        elif (status == 1):
            self.statusWidget_GantryConnectionStatus.setText("Connected")
            self.statusWidget_GantryConnectionStatus.setStyleSheet("color: green;")
        elif (status == 2):
            self.statusWidget_GantryConnectionStatus.setText("Connection in progress...")
            self.statusWidget_GantryConnectionStatus.setStyleSheet("color: orange;")
        elif (status == 3):
            self.statusWidget_GantryConnectionStatus.setText("Disconnection in progress...")
            self.statusWidget_GantryConnectionStatus.setStyleSheet("color: orange;")
    
    def updateGantryActionStatus(self, action):
        if (action == "disconnected"):
            self.statusWidget_GantryActionStatus.setText("Disconnected")
            self.statusWidget_GantryActionStatus.setStyleSheet("color: red;")
        elif (action == "none"):
            self.statusWidget_GantryActionStatus.setText("None")
            self.statusWidget_GantryActionStatus.setStyleSheet("color: green;")
        elif (action == "resetting"):
            self.statusWidget_GantryActionStatus.setText("Resetting Gantry...")
            self.statusWidget_GantryActionStatus.setStyleSheet("color: orange;")
        elif (action == "enabling"):
            self.statusWidget_GantryActionStatus.setText("Enabling motors...")
            self.statusWidget_GantryActionStatus.setStyleSheet("color: orange;")
        elif (action == "moving"):
            self.statusWidget_GantryActionStatus.setText("Moving...")
            #to X={} and Y={}...".format(location[0], location[1]))
            self.statusWidget_GantryActionStatus.setStyleSheet("color: orange;")
            pass
        elif (action == "referencing"):
            self.statusWidget_GantryActionStatus.setText("Referencing axes...")
            self.statusWidget_GantryActionStatus.setStyleSheet("color: orange;")


    def updateGantryCoords(self, coords):
        if coords == "NA":
            self.statusWidget_GantryCoords.setText("NA")
            self.statusWidget_GantryCoords.setStyleSheet("color: red;")
        else:
            self.statusWidget_GantryCoords.setText("X={};Y={}".format(coords[0],coords[1]))
            self.statusWidget_GantryCoords.setStyleSheet("color: green;")
    

    def updateCameraConnectionStatus(self, status):
        if (status == 0):
            self.cameraConnected = 0
            self.statusWidget_CameraConnectionStatus.setText("Disconnected")
            self.statusWidget_CameraConnectionStatus.setStyleSheet("color: red;")
            self.statusWidget_cameraActionStatus.setText("Disconnected")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: red;")
        elif (status == 1):
            self.cameraConnected = 0
            self.statusWidget_CameraConnectionStatus.setText("Connection Failed")
            self.statusWidget_CameraConnectionStatus.setStyleSheet("color: red;")
            self.statusWidget_cameraActionStatus.setText("Disconnected")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: red;")
        else:
            self.cameraConnected = 1
            self.statusWidget_CameraConnectionStatus.setText("{} - Connected".format(status))
            self.statusWidget_CameraConnectionStatus.setStyleSheet("color: green;")
            self.statusWidget_cameraActionStatus.setText("Connected")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: green;")


    def updateCameraDisplayStatus(self, status):
        if (status == 0):
            if (self.cameraConnected == 0):
                self.cameraDisplayed = 0
                self.statusWidget_cameraActionStatus.setText("Disconnected")
                self.statusWidget_cameraActionStatus.setStyleSheet("color: red;")
            elif (self.cameraConnected == 1):
                self.statusWidget_cameraActionStatus.setText("Connected")
                self.statusWidget_cameraActionStatus.setStyleSheet("color: green;")
        elif (status ==1):
            self.cameraDisplayed = 1
            if (self.cameraConnected == 1):
                self.statusWidget_cameraActionStatus.setText("Live Streaming")
                self.statusWidget_cameraActionStatus.setStyleSheet("color: orange;")
    
    def updateCameraCurrentAction(self, action):
        if (action == "Live Streaming"):
            self.statusWidget_cameraActionStatus.setText("Live Streaming")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: orange;")
        elif (action == "Disconnected"):
            self.statusWidget_cameraActionStatus.setText("Disconnected")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: red;")
        elif (action == "Capturing Screenshot"):
            self.statusWidget_cameraActionStatus.setText("Capturing Screenshot")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: orange;")
        elif (action == "Recording Video"):
            self.statusWidget_cameraActionStatus.setText("Recording Video")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: orange;")
        elif (action == "Saving Video"):
            self.statusWidget_cameraActionStatus.setText("Saving Video")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: orange;")
        elif (action == "Video Saved"):
            self.statusWidget_cameraActionStatus.setText("Video Saved")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: green;")
        elif (action == "Screenshot Saved"):
            self.statusWidget_cameraActionStatus.setText("Screenshot Saved")
            self.statusWidget_cameraActionStatus.setStyleSheet("color: green;")
