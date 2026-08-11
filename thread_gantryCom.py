# Import packages
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import queue
import re
import socket
import time

# Import local scripts
import gantry_commands

# Thread Class
class GantryCom(QThread):

    gantryConnectionSignal = pyqtSignal(int)
    gantryCoords = pyqtSignal(object)

    def __init__(self, gantryAddress, gantryConnectionStatus):
        super(GantryCom, self).__init__()
        # Gantry address
        self.gantryAddress = gantryAddress

        # Gantry connection status
        self.gantryConnectionStatus = gantryConnectionStatus

        # Gantry connection instruction
        self.endGantryConnection = False

        # Gantry command queue
        self.commandQueue = queue.Queue()

        # Gantry socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(2)


    def run(self):
        try:
            self.sock.connect(self.gantryAddress)
        except socket.timeout:
            print("ELLY:    Warning - Failed to connect to the gantry")
            self.endGantryConnection = True
        else:
            self.gantryConnectionSignal.emit(1)


        while self.endGantryConnection is False:
            try:
                self.sock.sendall(gantry_commands.keepAliveCMD)
                self.sock.recv(8192)
                gantrySummary = str(self.sock.recv(8192))
                jointCoords = re.findall(r"(?<=POSJOINTSETPOINT )(-?\d+.\d+)\s+(-?\d+.\d+)", gantrySummary)
                try:
                    self.gantryCoords.emit(jointCoords[0])
                except:
                    print("error")
                    pass
                time.sleep(0.1)
            except socket.error:
                print("ELLY:    Warning - Lost connection to the gantry")
                self.sock.close()
                self.gantryConnectionSignal.emit(0)
                time.sleep(0.1)
                print("ELLY:    Warning - Reconnecting to the gantry...")
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    self.sock.connect(self.gantryAddress)
                    self.gantryConnectionSignal.emit(1)
                    self.sock.sendall(gantry_commands.keepAliveCMD)
                    self.sock.recv(8192)
                    time.sleep(0.1)
                except socket.error:
                    print("ELLY:    Warning - Failed to connect to the gantry")
                    self.gantryConnectionSignal.emit(0)
                    self.endGantryConnection = True
                    time.sleep(0.1)
            
            try:
                command = self.commandQueue.get(False)
                print("ELLY:    Sending the following task to the gantry: ", command)
                self.sock.sendall(command)
                self.sock.recv(8192)
                self.commandQueue.task_done()
                time.sleep(0.1)
            except queue.Empty:
                time.sleep(0.1)
        self.sock.close()
        self.gantryConnectionSignal.emit(0)
        self.gantryCoords.emit("NA")


    def sendCommand(self, command):
        self.commandQueue.put(command)


    def stop(self):
        self.endGantryConnection = True
