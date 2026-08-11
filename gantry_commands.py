# GANTRY COMMAND LIST
# Keep Alive command
keepAliveMessage = "CRISTART 1234 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND"
keepAliveMessageEncoded = keepAliveMessage.encode('utf-8')
keepAliveCMD = bytearray(keepAliveMessageEncoded)

# Reset command
resetMessage = "CRISTART 1234 CMD Reset CRIEND"
resetMessageEncoded = resetMessage.encode('utf-8')
resetCMD = bytearray(resetMessageEncoded)

# Enable motors command
enableMotorsMessage = "CRISTART 1234 CMD Enable CRIEND"
enableMotorsMessageEncoded = enableMotorsMessage.encode('utf-8')
enableMotorsCMD = bytearray(enableMotorsMessageEncoded)

# Set Client Active command
setClientActiveMessage = "CRISTART 1234 CMD SetActive true CRIEND"
setClientActiveMessageEncoded = setClientActiveMessage.encode('utf-8')
setClientActiveCMD = bytearray(setClientActiveMessageEncoded)

# Move to X=5 and Y=5 command
moveGantryTo5_5Message = "CRISTART 1234 CMD Move Joint 5 5 0 0 0 0 0 0 0 30 CRIEND"
moveGantryTo5_5MessageEncoded = moveGantryTo5_5Message.encode('utf-8')
moveGantryTo5_5CMD = bytearray(moveGantryTo5_5MessageEncoded)

# Reference axes command
referenceAxesMessage = "CRISTART 1234 CMD ReferenceAllJoints CRIEND"
referenceAxesMessageEncoded = referenceAxesMessage.encode('utf-8')
referenceAxesCMD = bytearray(referenceAxesMessageEncoded)

# Define Motion Type to Joint command
motionTypeJointMessage = "CRISTART 1234 CMD MotionTypeJoint CRIEND"
motionTypeJointMessageEncoded = motionTypeJointMessage.encode('utf-8')
motionTypeJointCMD=bytearray(motionTypeJointMessageEncoded)

# Function move to specified X and Y command
def moveTo(x, y):
    moveMessage = "CRISTART 1234 CMD Move Joint {} {} 0 0 0 0 0 0 0 30 CRIEND".format(x, y)
    moveMessageEncoded = moveMessage.encode('utf-8')
    moveCMD = bytearray(moveMessageEncoded)
    return moveCMD
