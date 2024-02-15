import os
import math
import pandas as pd
import numpy as np
import json
from backend.constants import *
from main import userCity, userCountry,userCounty, userState, buildingArea, userZipcode

userData = {
    "buildingType" : "OLg",
    "yearBuilt" : 1976,
    "CZinfo" : 16,
}
RetroDataDict = {}

Retro_DB_Path = os.path.join(cwd, "backend",  "database", "XXX.csv")
databaseRetro = pd.read_csv(Retro_DB_Path)


def getRetroData(userData):
    filteredRetroDB = databaseRetro[(databaseRetro["Building Type"] == userData["buildingType"]) and \
                                (databaseRetro["Building Vintage"] == userData["yearBuilt"]) and \
                                (databaseRetro["Climate Zone"] == userData["CZinfo"])]
    if len(filteredRetroDB) == 1:
        RetroDataDict["MOTOR-FAN"] =  filteredRetroDB['HW Pump Flow [GPM]']
        RetroDataDict["PACKAGED-HVAC"] = filteredRetroDB['Heating (Natural Gas - kWh)'] + \
                                         filteredRetroDB['Design Cooling Capacity [tons]'] + \
                                         filteredRetroDB["Design Heating Capacity [kBtu]"]
        return RetroDataDict
    else:
        return "Retro Model Configuration Failed"
    