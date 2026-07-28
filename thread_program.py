# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime
import os
import time

# Import local scripts


class ProgramThread(QThread):

    programGantrySignal = pyqtSignal(object)
    programArduinoSignal = pyqtSignal(object)
    programCameraSignal = pyqtSignal(object)

    def __init__(self, useGantry, useCamera, useRingLight, timesDF, moveCommands, recordVideo, videoDuration, videoDirectory):
        super().__init__()
        # Loading variables passed in the class
        self.useGantry = useGantry
        self.useCamera = useCamera
        self.useRingLight = useRingLight
        self.timesDF = timesDF  # These are the different times at which to loop the gantry
        self.moveCommands = moveCommands  # These are the different location coordinates where to move the gantry within each loop
        if recordVideo is True:
            self.recordVideo = True  # This evaluates whether we required the system to make a video at each location
        else:
            self.recordVideo = False
        self.videoDuration = videoDuration  # This is the video duration
        self.videoDirectory = videoDirectory  # This is the directory where to save the videos
        self.loopCounter = 0  # This counter evaluates whether or not all loops (one loop per time input) were performed

    def run(self):
        print("ELLY:    Starting my automated program composed of {} time loops".format(len(self.timesDF)))
        print("ELLY:    Next loop planned at: {}".format(self.timesDF[self.loopCounter]))
        while self.loopCounter < len(self.timesDF):
            now = datetime.now()
            now = str(now)
            if now.startswith(self.timesDF[self.loopCounter]):
                print("ELLY:    Starting loop {}/{}".format(self.loopCounter+1, len(self.timesDF)))
                print("ELLY:    Loop time is: {} and current time is {}".format(self.timesDF[self.loopCounter], now))

                # If gantry is required, we run the camera and ring light loop within the gantry loop
                if self.useGantry is True:
                    # Connecting the gantry
                    print("ELLY:    Connecting to the gantry")
                    self.programGantrySignal.emit(["Connect"])
                    time.sleep(5)
                    # Referencing the gantry
                    print("ELLY:    Aligning gantry axes")
                    self.programGantrySignal.emit(["Reference"])
                    # Put Thread on sleep for 50 seconds for the gantry to finalize its initialization
                    time.sleep(50)
                    for i in range(len(self.moveCommands)):
                        moveCommand = self.moveCommands[i]
                        patchXcoordinate = moveCommand[0]
                        patchYcoordinate = moveCommand[1]
                        movingTime = moveCommand[2]
                        patchID = moveCommand[3]
                        print("ELLY:    Moving gantry to {} (X={};Y={})".format(patchID, patchXcoordinate, patchYcoordinate))
                        self.programGantrySignal.emit(["Move", patchXcoordinate, patchYcoordinate, movingTime])
                        time.sleep(movingTime + 2)
                        if self.useCamera is True:
                            if self.recordVideo is True:
                                if self.useRingLight is True:
                                    # First connect to the Arduino
                                    print("ELLY:    Connecting to the Arduino (Ring Light)")
                                    self.programArduinoSignal.emit(["Connect Arduino"])
                                    time.sleep(5)
                                    # Then swith on the ring light linked to the Arduino
                                    print("ELLY:    Turning ON the Ring Light (Arduino)")
                                    self.programArduinoSignal.emit(["Turn Light On"])
                                    time.sleep(2)
                                # Then connect to the camera
                                print("ELLY:    Connecting to the camera")
                                self.programCameraSignal.emit(["Connect Camera"])
                                time.sleep(5)
                                # Then start video recording
                                print("ELLY:    Recording video (duration: {})".format(self.videoDuration))
                                self.programCameraSignal.emit(["Start Video Recording", self.videoDuration])
                                time.sleep(self.videoDuration + 5)
                                # Then disconnect the camera
                                print("ELLY:    Disconnecting the camera")
                                self.programCameraSignal.emit(["Disconnect Camera"])
                                time.sleep(2)
                                if self.useRingLight is True:
                                    # Then swith off the ring light linked to the Arduino
                                    print("ELLY:    Turning OFF the Ring Light (Arduino)")
                                    self.programArduinoSignal.emit(["Turn Light Off"])
                                    time.sleep(2)
                                    # Then disconnect to the Arduino
                                    print("ELLY:    Disconnecting the Arduino (Ring Light)")
                                    self.programArduinoSignal.emit(["Disconnect Arduino"])
                                    time.sleep(2)
                                # Then save the video
                                videoDate, videoTime = self.timesDF[self.loopCounter].split(" ")
                                videoYear, videoMonth, videoDay = videoDate.split("-")
                                videoHour, videoMinute = videoTime.split(":")
                                videoName = str(videoYear + "_" + videoMonth + "_" + videoDay + "_" + videoHour + "_" + videoMinute + "_" + patchID)
                                videoPath = os.path.join(self.videoDirectory, videoName)
                                print("ELLY:    Saving the video {}".format(videoPath))
                                self.programCameraSignal.emit(["Save Video", self.videoDuration, videoPath])
                                time.sleep(4*self.videoDuration)
                                print("ELLY:    Finished all actions related to {} at time {}".format(patchID, self.timesDF[self.loopCounter]))
                                time.sleep(1)
                    print("ELLY:    Finished loop {}/{}".format(self.loopCounter+1, len(self.timesDF)))
                    # Disconnecting the gantry
                    print("ELLY:    Disconnecting the gantry")
                    self.programGantrySignal.emit(["Disconnect"])
                    time.sleep(1)
                elif self.useGantry is False:
                    if self.useCamera is True:
                        if self.recordVideo is True:
                            if self.useRingLight is True:
                                # First connect to the Arduino
                                print("ELLY:    Connecting to the Arduino (Ring Light)")
                                self.programArduinoSignal.emit(["Connect Arduino"])
                                time.sleep(5)
                                # Then swith on the ring light linked to the Arduino
                                print("ELLY:    Turning ON the Ring Light (Arduino)")
                                self.programArduinoSignal.emit(["Turn Light On"])
                                time.sleep(2)
                            # Then connect to the camera
                            print("ELLY:    Connecting to the camera")
                            self.programCameraSignal.emit(["Connect Camera"])
                            time.sleep(5)
                            # Then start video recording
                            print("ELLY:    Recording video (duration: {})".format(self.videoDuration))
                            self.programCameraSignal.emit(["Start Video Recording", self.videoDuration])
                            time.sleep(self.videoDuration + 5)
                            # Then disconnect the camera
                            print("ELLY:    Disconnecting the camera")
                            self.programCameraSignal.emit(["Disconnect Camera"])
                            time.sleep(2)
                            if self.useRingLight is True:
                                # Then swith off the ring light linked to the Arduino
                                print("ELLY:    Turning OFF the Ring Light (Arduino)")
                                self.programArduinoSignal.emit(["Turn Light Off"])
                                time.sleep(2)
                                # Then disconnect to the Arduino
                                print("ELLY:    Disconnecting the Arduino (Ring Light)")
                                self.programArduinoSignal.emit(["Disconnect Arduino"])
                                time.sleep(2)
                            # Then save the video
                            videoDate, videoTime = self.timesDF[self.loopCounter].split(" ")
                            videoYear, videoMonth, videoDay = videoDate.split("-")
                            videoHour, videoMinute = videoTime.split(":")
                            videoName = str(videoYear + "_" + videoMonth + "_" + videoDay + "_" + videoHour + "_" + videoMinute)
                            videoPath = os.path.join(self.videoDirectory, videoName)
                            print("ELLY:    Saving the video {}".format(videoPath))
                            self.programCameraSignal.emit(["Save Video", self.videoDuration, videoPath])
                            time.sleep(4*self.videoDuration)
                            print("ELLY:    Finished all actions related to time {}".format(self.timesDF[self.loopCounter]))
                            time.sleep(1)

                self.loopCounter += 1
                if (self.loopCounter+1 <= len(self.timesDF)):
                    print("ELLY:    Next loop planned at: {}".format(self.timesDF[self.loopCounter]))
            else:
                # print(now)
                time.sleep(1)
        print("ELLY:    My automated program is finished!")
