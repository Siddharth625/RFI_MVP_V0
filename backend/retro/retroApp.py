import os
import math
import pandas as pd
import numpy as np
import json
from backend.constants import *

userData = {
    "buildingType" : "OLg",
    "yearBuilt" : 1976,
    "CZinfo" : 16,
}
RETRO_DATA_DICT = {
        "1975" : {
                "CZ03" : {
                        "OLs" : {
                                    "BuildingArea" : 10010,
                                    "HVAC Fan (hp)" : 13.94,
                                    "Design Cooling Capacity [tons]" : 29.36, 
                                }
                         }
                 }
}

# RETRO_DATA_DICT = {
#         "2017" : {
#                 "CZ04" : {
#                         "OfL" : {
#                                     "BuildingArea" : 174960,
#                                     "HVAC Fan (hp)" : 152,
#                                     "Design Cooling Capacity [tons]" : 258, 
#                                 }
#                          }
#                  }
# }
                

RetroDataDB = {}

# Retro_DB_Path = os.path.join(cwd, "backend",  "database", "XXX.csv")
# databaseRetro = pd.read_csv(Retro_DB_Path)


def getRetroData(userData):
    filteredRetroDB = databaseRetro[(databaseRetro["Building Type"] == userData["buildingType"]) and \
                                (databaseRetro["Building Vintage"] == userData["yearBuilt"]) and \
                                (databaseRetro["Climate Zone"] == userData["CZinfo"])]
    if len(filteredRetroDB) == 1:
        RetroDataDB["MOTOR-FAN"] =  filteredRetroDB['HVAC Fan (hp)']
        RetroDataDB["PACKAGED-HVAC"] = filteredRetroDB['Design Cooling Capacity [tons]']
        RetroDataDB["MOTOR-PUMP-HW"] = filteredRetroDB["HW Pump (hp)"]
        RetroDataDB["MOTOR-PUMP-CHW"] = filteredRetroDB["CHW Pump (hp)"]
        RetroDataDB["HVAC-ELEC"] = filteredRetroDB["Cooling (kWh)"] + \
                                     filteredRetroDB["Fans (kWh)"] + \
                                     filteredRetroDB["Pumps (kWh)"]
        return RetroDataDB
    else:
        return "Retro Model Configuration Failed"
    