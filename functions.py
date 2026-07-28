# Import packages
import pandas as pd

# Import local scripts

def getStartingTimes(startingTimes):
    data = pd.read_csv(startingTimes, sep="\t", header=None)
    data.columns = ["Time"]
    startingTimesList = data["Time"].tolist()
    return startingTimesList


def getMoveCommands(locations):
    data = pd.read_csv(locations, sep="\t", header=None)
    data.columns = ["X", "Y", "MovingTime", "PatchID"]
    dataList = [[x, y, time, patch] for x, y, time, patch in zip(data["X"], data["Y"], data["MovingTime"], data["PatchID"])]
    return dataList