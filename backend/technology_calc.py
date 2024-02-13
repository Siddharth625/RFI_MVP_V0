import os
import math
import pandas as pd
import numpy as np
import json
from backend.constants import *

class Technology:
    def __init__(self) -> None:
        pass

    def Standard_Type(self, utpDF, buildingArea):
        resdf = utpDF.copy()
        resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "STANDARD",
                                  resdf["Incentive Value"],
                                  0)
        assumption_transformation_df = resdf[resdf["Assumption Type"] == "STANDARD"]
        return assumption_transformation_df


    def HVAC_Motors (self, df_master, utpDF, buildingArea):
        print(utpDF.columns)
        resdffan = utpDF[utpDF["Sub-Technology"] == "MOTOR-FAN"]
        resdffan["Amt_Estimation"] = np.where(resdffan["Assumption Type"] == "HVAC_MOTOR_HP",
                                  resdffan["Incentive Value"] * RETRO_MOTOR_FAN_HP * buildingArea,
                                  0)
        df_add = resdffan[resdffan["Sub-Technology"] == "MOTOR-FAN"]
        df_master = pd.concat([df_master ,df_add], ignore_index=True)
        return df_master

    def HVAC_PACKAGED(self, df_master, utpDF, buildingArea):
        if buildingArea <= 50000:
            avg_ton = 1
        elif buildingArea > 50000 and buildingArea <= 100000:
            avg_ton = 2
        elif buildingArea > 100000 and buildingArea <= 150000:
            avg_ton = 3
        resdf = utpDF[utpDF["Sub-Technology"] == "PACKAGED-HVAC"]
        resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "HVAC_PACKAGED_TON",
                                  resdf["Incentive Value"] *  avg_ton * RETRO_HVAC_PACKAGED_W * buildingArea,
                                  0)
        df_add = resdf[resdf["Assumption Type"] == "HVAC_PACKAGED_TON"]
        df_master = pd.concat([df_master ,df_add], ignore_index=True)
        return df_master

        
        
