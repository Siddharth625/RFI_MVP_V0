import os
import math
import pandas as pd
import numpy as np
import json
from backend.constants import *
from backend.retro.retroApp import RETRO_DATA_DICT

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
                                  resdffan["Incentive Value"] * RETRO_DATA_DICT['1975']['CZ03']['OLs']['HVAC Fan (hp)'] \
                                  *(buildingArea / RETRO_DATA_DICT['1975']['CZ03']['OLs']['BuildingArea']),
                                  resdffan["Max Amount"])
        df_add = resdffan[resdffan["Sub-Technology"] == "MOTOR-FAN"]
        df_master = pd.concat([df_master ,df_add], ignore_index=True)
        return df_master

    # def HVAC_PACKAGED(self, df_master, utpDF, buildingArea):
    #     avg_ton = 5
    #     resdf = utpDF[utpDF["Sub-Technology"] == "PACKAGED-HVAC"]
    #     resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "HVAC_PACKAGED_TON",
    #                               resdf["Incentive Value"]  * RETRO_DATA_DICT['1975']['CZ03']['OLs']['Design Cooling Capacity [tons]'] \
    #                               *(buildingArea / RETRO_DATA_DICT['1975']['CZ03']['OLs']['BuildingArea']) , # Need a building scaling factor
    #                               resdf["Max Amount"])
    #     df_add = resdf[resdf["Assumption Type"] == "HVAC_PACKAGED_TON"]
    #     df_master = pd.concat([df_master ,df_add], ignore_index=True)
    #     return df_master

    def HVAC_PACKAGED(self, df_master, utpDF, buildingArea):
        resdf = utpDF[utpDF["Sub-Technology"] == "PACKAGED-HVAC"]
        calculated_amount = resdf["Incentive Value"] * RETRO_DATA_DICT['1975']['CZ03']['OLs']['Design Cooling Capacity [tons]'] \
                            * (buildingArea / RETRO_DATA_DICT['1975']['CZ03']['OLs']['BuildingArea'])
        resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "HVAC_PACKAGED_TON",
                                        np.where(calculated_amount > resdf["Max Amount"],
                                                    resdf["Max Amount"],
                                                    calculated_amount),
                                        resdf["Max Amount"])
        df_add = resdf[resdf["Assumption Type"] == "HVAC_PACKAGED_TON"]
        df_master = pd.concat([df_master, df_add], ignore_index=True)
        return df_master
        
        
