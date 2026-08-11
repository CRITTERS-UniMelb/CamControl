# Import packages
import cv2
import imutils
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Import local scripts


class CameraThread(QThread):

    cameraImage = pyqtSignal(object)
    cameraNameSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.cameraName = None
        self.hcam = None
        self.buf = None
        self.running = False

    def connectCamera(self):
        self.hcam = cv2.VideoCapture(0)
        self.running = True
        self.cameraName = 'Webcam'
        self.cameraNameSignal.emit(self.cameraName)
        self.width = 500
        self.height = 500
        self.imageMinimizedWidth = 500
        self.imageMinimizedHeight = 500

    def run(self):
        self.connectCamera()
        while self.running:
            ret,frame = self.hcam.read()
            if ret:
                self.frame = frame.copy()
                frame = self.cvimage_to_label(frame)
                self.cameraImage.emit(frame)
        if self.hcam:
            self.hcam.release()
        
    def cvimage_to_label(self,image):
        image = imutils.resize(image,width = 640)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image = QImage(image,
                       image.shape[1],
                       image.shape[0],
                       QImage.Format.Format_RGB888)
        return image


    def stop(self):
        self.running = False
        self.cameraNameSignal.emit(0)
        print("ELLY:    Camera disconnected")
        self.quit()
        self.wait()
        
            