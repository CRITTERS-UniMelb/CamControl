# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import os

# Import local scripts


class VideoRecorder(QThread):

    currentAction = pyqtSignal(object)

    def __init__(self, videoPackage, videoPath, encodingMethod):
        super().__init__()
        self.cameraFrames = videoPackage[0]
        self.fps = len(videoPackage[0])/(videoPackage[2]-videoPackage[1])
        self.videoPath = videoPath
        self.encodingMethod = encodingMethod
        self.cv2CameraFrames = []
    
    @staticmethod
    def convertQImageToMat(incomingImage):
        # Horizontal mirroring
        incomingImage = incomingImage.mirrored(False,True)
        # QImage first conversion
        incomingImage = incomingImage.convertToFormat(QImage.Format_RGBX8888)
        ptr = incomingImage.constBits()
        ptr.setsize(incomingImage.byteCount())
        # QImage conversion to numpy array (openCV image format)
        cv_im_in = np.array(ptr, copy=True).reshape(incomingImage.height(), incomingImage.width(), 4)
        cv_im_in = cv2.cvtColor(cv_im_in, cv2.COLOR_BGRA2RGB)
        return cv_im_in


    def run(self):
        # Solution 1
        self.currentAction.emit("Converting Frames...")
        for i in range(len(self.cameraFrames)):
            if (i == 0):
                width = self.cameraFrames[i].width()
                height = self.cameraFrames[i].height()
                size = (width, height)
            # Code to activate if willing to save image frames
            imageNumber = "{0:06d}".format(i)
            self.cameraFrames[i].save("snapshots/frame{}.jpg".format(imageNumber))
            cv2Frame = self.convertQImageToMat(self.cameraFrames[i])
            self.cv2CameraFrames.append(cv2Frame)
        self.currentAction.emit("Saving video...")
        if self.encodingMethod == 1:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        else:
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

        output = cv2.VideoWriter(self.videoPath, fourcc, self.fps, size)

        # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        # fourcc = cv2.VideoWriter_fourcc(*'H264')
        # fourcc = cv2.VideoWriter_fourcc(*'avc1')
        # output = cv2.VideoWriter("test3.mp4", fourcc, self.fps, size)

        for i in range(len(self.cv2CameraFrames)):
            output.write(self.cv2CameraFrames[i])
        output.release()
        self.cv2CameraFrames = []
        self.currentAction.emit("Video saved")


        # # This is another working solution that first save images
        # # First Save the images
        # for i in range(len(self.cameraFrames)):
        #     image = self.cameraFrames[i]
        #     image = image.mirrored(False,True)
        #     if (self.counter == 1):
        #         width = image.width()
        #         height = image.height()
        #         size = (width, height)
        #     imageNumber = "{0:06d}".format(self.counter)
        #     image.save("frame/frame{}.jpg".format(imageNumber))
        #     self.counter += 1
        
        # # Then load the images with openCV and save them as video
        # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        # output = cv2.VideoWriter("test.avi", fourcc, self.fps, size)
        # for image in os.listdir("frame"):
        #     if image.endswith(".jpg"):
        #         imagePath = os.path.join("frame", image)
        #         img = cv2.imread(imagePath)
        #         # img = cv2.flip(img, 0)
        #         output.write(img)
        # output.release()
