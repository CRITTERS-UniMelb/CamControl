#!/usr/bin/env python
# coding: utf-8
'''
Created on 2024-08-19
@author:fdy
'''

import ctypes
from ctypes import *
from TUCam import *
from enum import Enum
import time

# the call back fuction
class CallBack():
    def __init__(self, TUCAMOPEN_PARA):
        self.TUCAMOPEN = TUCAMOPEN_PARA
        self.s_frameCounter = c_int32
        self.s_frameCounter = 0
    def OnCallbackNewFrame(self):
        frame = TUCAM_RAWIMG_HEADER()
        self.s_frameCounter += 1;
        print('Frame %d has been arrived' %self.s_frameCounter)
        try:
            # ch:回调获取数据流 | en:Callback get stream
            Result = TUCAM_Buf_GetData(self.TUCAMOPEN.hIdxTUCam, pointer(frame))
            print('Frame info: index-%d, imageSize-%d, width-%d, height-%d' %(frame.uiIndex,frame.uiImgSize,frame.usWidth,frame.usHeight))

        except Exception:
            print('except')

class Tucam():
    def __init__(self):
        self.Path = './'
        self.TUCAMINIT = TUCAM_INIT(0, self.Path.encode('utf-8'))
        TUCAM_Api_Init(pointer(self.TUCAMINIT), 1000)
        self.count = self.TUCAMINIT.uiCamCount
        self.TUCAMOPEN = TUCAM_OPEN(0, 0)

        if self.TUCAMINIT.uiCamCount == 0:
            print('No Camera found!')
            return
        print('Connected %d camera' %self.TUCAMINIT.uiCamCount)

    def OpenCamera(self, Idx):

        if  Idx >= self.TUCAMINIT.uiCamCount:
            return

        self.TUCAMOPEN = TUCAM_OPEN(Idx, 0)

        TUCAM_Dev_Open(pointer(self.TUCAMOPEN))

        if 0 == self.TUCAMOPEN.hIdxTUCam:
            print('Open the camera failure')
            return
        else:
            print('Open the camera success')

    def StartCapture(self):
        self.m_frame = TUCAM_FRAME()
        m_frformat= TUFRM_FORMATS
        m_capmode = TUCAM_CAPTURE_MODES

        self.m_frame.pBuffer     = 0
        self.m_frame.ucFormatGet = m_frformat.TUFRM_FMT_USUAl.value
        self.m_frame.uiRsdSize   = 1

        # Allocate frame memory assuming
        TUCAM_Buf_Alloc(self.TUCAMOPEN.hIdxTUCam, pointer(self.m_frame))
        TUCAM_Cap_Start(self.TUCAMOPEN.hIdxTUCam, m_capmode.TUCCM_SEQUENCE.value)

    def StopCapture(self):
        TUCAM_Buf_AbortWait(self.TUCAMOPEN.hIdxTUCam)
        TUCAM_Cap_Stop(self.TUCAMOPEN.hIdxTUCam)
        TUCAM_Buf_Release(self.TUCAMOPEN.hIdxTUCam)

    def CloseCamera(self):
        # 7.ch:关闭相机 | en:Close the camera
        TUCAM_Dev_Close(self.TUCAMOPEN.hIdxTUCam)
        print('Close the camera success')

if __name__ == '__main__':
    # 1.ch:初始化sdk api | en:Init the sdk api
    demo = Tucam()
    # 2.ch:打开第一个相机 | en:Open the first camera
    demo.OpenCamera(0)

    if 0 != demo.TUCAMOPEN.hIdxTUCam:
        m_callback = CallBack(demo.TUCAMOPEN)
        CALL_BACK_FUN = BUFFER_CALLBACK(m_callback.OnCallbackNewFrame)
        CALL_BACK_USER = CONTEXT_CALLBACK(m_callback.__class__)
        # 3. ch:注册回调函数将获取到新数据 | en:Register the callback function that will be called by tucam when new raw frame arrives
        TUCAM_Buf_DataCallBack(demo.TUCAMOPEN.hIdxTUCam, CALL_BACK_FUN, CALL_BACK_USER)

        # 4.ch:开始采集 | en:Start capture
        demo.StartCapture()

        # 5.ch:循环采集10张图 | en:Loop acquiring 10 images
        count = 10
        for i in range(count):
            # If necessary, we can wait here for the frames after image processing to be read out
            Result = TUCAM_Buf_WaitForFrame(demo.TUCAMOPEN.hIdxTUCam, pointer(demo.m_frame), 1000)

        # 6.ch:停止采集 | en:Stop capture
        demo.StopCapture()

        # 7.ch:关闭相机 | en:Close the camera
        demo.CloseCamera()
    TUCAM_Api_Uninit()