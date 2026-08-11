# Import packages
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Import local scripts


# QPushButton styles
# background-color:lightgray;
def getQPushButtonStyle1(size):
    QPushButton_Style1 = f"""
                QPushButton {{
                                font-weight: bold;
                                border-radius:{size};
                                border:1px solid gray;
                                background-color:white;
                                text-align:center
                            }}
                QPushButton::hover {{  
                                font-weight: bold;
                                border-radius:{size};
                                border:1px solid CornflowerBlue;
                                background-color:AliceBlue;
                                text-align:center
                            }}
                QPushButton::pressed {{
                                font-weight: bold;
                                border-radius:{size};
                                border:2px solid RoyalBlue;
                                background-color:LightSkyBlue
                            }}
            """
    return QPushButton_Style1

def getQPushButtonStyle1_shadow():
    shadow = QGraphicsDropShadowEffect()
    shadow.setColor(QColor(0, 0, 0, 255*0))
    shadow.setOffset(2)
    shadow.setBlurRadius(15)
    return shadow


# creating VLine class
class VLine(QFrame):
  
    # a simple Vertical line
    def __init__(self):
        super().__init__()
        self.setFrameShape(self.Shape.VLine)
        self.setFrameShadow(self.Shadow.Sunken)


# creating HLine class
class HLine(QFrame):
  
    # a simple Horizontal line
    def __init__(self):
        super().__init__()
        self.setFrameShape(self.Shape.HLine)
        self.setFrameShadow(self.Shadow.Sunken)