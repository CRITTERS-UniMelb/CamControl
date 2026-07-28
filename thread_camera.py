# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import pythoncom
import time
import uvcham

# Import local scripts


class CameraThread(QThread):

    cameraImage = pyqtSignal(object)
    cameraNameSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.cameraName = None
        self.hcam = None
        self.buf = None
        self.autoExposure = True

    def connectCamera(self):
        try:
            a = uvcham.Uvcham.enum()
        except:
            print("ELLY:    Warning - Failed to find a camera")
            self.cameraName = None
            self.cameraNameSignal.emit(self.cameraName)
        else:
            if len(a) <= 0:
                print("ELLY:    Warning - Failed to find a camera")
                self.cameraName = None
                self.cameraNameSignal.emit(self.cameraName)
            else:
                try:
                    hcam = uvcham.Uvcham.open(a[0].id)
                except uvcham.HRESULTException as ex:
                    print("ELLY:    Warning - Failed to open the camera, hr=0x{:x}".format(ex.hr))
                    self.cameraName = None
                    self.cameraNameSignal.emit(self.cameraName)
                else:
                    self.cameraName = a[0].displayname
                    print("ELLY:    Found the camera {}".format(self.cameraName))
                    self.cameraNameSignal.emit(str(self.cameraName))


    @staticmethod
    def cameraCallback(nEvent, ctx):
        ctx.CameraCallback(nEvent)


    def CameraCallback(self, nEvent):
        if nEvent == uvcham.UVCHAM_EVENT_IMAGE:
            img = QImage(self.buf, self.width, self.height, (self.width * 24 + 31) // 32 * 4, QImage.Format_BGR888)
            self.cameraImage.emit(img)
        else:
            pass
            # print('event callback: {}'.format(nEvent))


    def run(self):
        #pythoncom.CoInitialize()
        a = uvcham.Uvcham.enum()
        if len(a) > 0:
            print("ELLY:    Opening the camera {} (id = {})".format(a[0].displayname, a[0].id))
            self.hcam = uvcham.Uvcham.open(a[0].id)
            if self.hcam:
                try:
                    res = self.hcam.get(uvcham.UVCHAM_RES)
                    self.width = self.hcam.get(uvcham.UVCHAM_WIDTH | res)
                    self.height = self.hcam.get(uvcham.UVCHAM_HEIGHT | res)
                    bufsize = ((self.width * 24 + 31) // 32 * 4) * self.height
                    print("ELLY:    Camera image size: {} x {}, bufsize = {}".format(self.width, self.height, bufsize))
                    self.buf = bytes(bufsize)
                    if self.buf:
                        try:
                            self.hcam.start(self.buf, self.cameraCallback, self)
                        except uvcham.HRESULTException as ex:
                            print("ELLY:    Warning - Failed to start the camera, hr=0x{:x}".format(ex.hr))
                    input("")
                    # input("ELLY:    press ENTER to exit")
                finally:
                    self.hcam.close()
                    self.hcam = None
                    self.buf = None
            else:
                print("ELLY:    Warning - Failed to open the camera")
        else:
            print("ELLY:    Warning - Failed to find the camera")
        

    def changeAutoExposure(self, state):
        if self.hcam is not None:
            if state is True:
                self.hcam.put(uvcham.UVCHAM_AEXPO, 1)
                print("ELLY:    Camera Auto Exposure Enabled")
                self.autoExposure = True
            elif state is False:
                self.hcam.put(uvcham.UVCHAM_AEXPO, 0)
                print("ELLY:    Camera Auto Exposure Disabled")
                self.autoExposure = False
    
    def changeExposureTime(self, time):
        if self.hcam is not None:
            if self.autoExposure is False:
                self.hcam.put(uvcham.UVCHAM_EXPOTIME, time)


    def stop(self):
        try:
            self.hcam
        except:
            pass
        else:
            self.hcam.close()
            self.cameraName = None
            self.cameraNameSignal.emit(0)
            print("ELLY:    Camera disconnected")
            