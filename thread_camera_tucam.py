# Import packages
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from sys import platform

# Import local scripts
if platform == "win32":
  import tucam_cmds



class CameraThread_uvc(QThread):

    cameraImage = pyqtSignal(object)
    cameraNameSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.cameraName = None
        self.running = False
        self.hcam = None
        self.buf = None
        self.autoExposure = True

    def connectCamera(self):
        try:
            a = tucam_cmds.Tucam()
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
                    hcam = tucam_cmds.Tucam.OpenCamera(0) 
                except uvcham.HRESULTException as ex:
                    print("ELLY:    Warning - Failed to open the camera, hr=0x{:x}".format(ex.hr))
                    self.cameraName = None
                    self.cameraNameSignal.emit(self.cameraName)
                else:
                    self.cameraName = a.hIdxTUCam
                    print("ELLY:    Found the camera {}".format(self.cameraName))
                    self.cameraNameSignal.emit(str(self.cameraName))

    def callback(self):
        

    def run(self):
        a = tucam_cmds.Tucam()
        a.OpenCamera(0)
        while self.running is True:
            m_callback = tucam_cmds.CallBack(a.TUCAMOPEN)
            CALL_BACK_FUN = BUFFER_CALLBACK(m_callback.OnCallbackNewFrame)
            CALL_BACK_USER = CONTEXT_CALLBACK(m_callback.__class__)
            # 3. ch:注册回调函数将获取到新数据 | en:Register the callback function that will be called by tucam when new raw frame arrives
            TUCAM_Buf_DataCallBack(a.TUCAMOPEN.hIdxTUCam, CALL_BACK_FUN, CALL_BACK_USER)
            # 4.ch:开始采集 | en:Start capture
            a.StartCapture()
            # 6.ch:停止采集 | en:Stop capture
            demo.StopCapture()
            # 7.ch:关闭相机 | en:Close the camera
            demo.CloseCamera()

        pythoncom.CoInitialize()
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
            