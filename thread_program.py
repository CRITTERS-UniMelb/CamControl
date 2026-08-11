# Import packages
import os
import time
from datetime import datetime

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

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
        print(f"ELLY:    Starting my automated program composed of {len(self.timesDF)} time loops")
        print(f"ELLY:    Next loop planned at: {self.timesDF[self.loopCounter]}")
        while self.loopCounter < len(self.timesDF):
            now = datetime.now().astimezone()
            now = str(now)
            if now.startswith(self.timesDF[self.loopCounter]):
                print(f"ELLY:    Starting loop {self.loopCounter+1}/{len(self.timesDF)}")
                print(f"ELLY:    Loop time is: {self.timesDF[self.loopCounter]} and current time is {now}")

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
                        print(f"ELLY:    Moving gantry to {patchID} (X={patchXcoordinate};Y={patchYcoordinate})")
                        self.programGantrySignal.emit(["Move", patchXcoordinate, patchYcoordinate, movingTime])
                        time.sleep(movingTime + 2)
                        if (self.useCamera is True) and (self.recordVideo is True):
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
                            print(f"ELLY:    Recording video (duration: {self.videoDuration})")
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
                            print(f"ELLY:    Saving the video {videoPath}")
                            self.programCameraSignal.emit(["Save Video", self.videoDuration, videoPath])
                            time.sleep(4*self.videoDuration)
                            print(f"ELLY:    Finished all actions related to {patchID} at time {self.timesDF[self.loopCounter]}")
                            time.sleep(1)
                    print(f"ELLY:    Finished loop {self.loopCounter+1}/{len(self.timesDF)}")
                    # Disconnecting the gantry
                    print("ELLY:    Disconnecting the gantry")
                    self.programGantrySignal.emit(["Disconnect"])
                    time.sleep(1)
                elif self.useGantry is False:
                    if (self.useCamera is True) and (self.recordVideo is True):
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
                        print(f"ELLY:    Recording video (duration: {self.videoDuration})")
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
                        print(f"ELLY:    Saving the video {videoPath}")
                        self.programCameraSignal.emit(["Save Video", self.videoDuration, videoPath])
                        time.sleep(4*self.videoDuration)
                        print(f"ELLY:    Finished all actions related to time {self.timesDF[self.loopCounter]}")
                        time.sleep(1)

                self.loopCounter += 1
                if (self.loopCounter+1 <= len(self.timesDF)):
                    print(f"ELLY:    Next loop planned at: {self.timesDF[self.loopCounter]}")
            else:
                # print(now)
                time.sleep(1)
        print("ELLY:    My automated program is finished!")
