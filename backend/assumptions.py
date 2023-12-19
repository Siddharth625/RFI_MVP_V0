import os
import pandas as pd
import numpy as np
from backend.constants import *

# Energy Breakup for a small office
HVAC_SO_EUI = 4.95
LED_SO_EUI = 1.8
INSULATION_SO_EUI = 0.9
CONTROLS_SO_EUI = 1.35
TOTAL_SO_EUI = 9



# HVAC Type 1
ASMP_BTUH_SCALING_FACTOR = 5 # Needs Revision

# HVAC Type 2
KWH_TO_BTU = 3414
HVAC_Breakup = {
    "Air Conditioners" : 0.6,
    "Air Compressors" : 0.6,
    "Heat Pumps" : 0.6,
    "Heaters" : 0.6,
    "Pumps and Motors" : 0.3,

}

class Assumptions:
    def __init__(self) -> None:
        pass

    def HVAC_TYPE_1(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "HVAC Type 1", \
                                  resdf["Incentive Value"] * ASMP_BTUH_SCALING_FACTOR, \
                                  resdf["Incentive Value"])
        return resdf
        
    
    def HVAC_TYPE_2(self, resdf):
        """_summary_

        Args:
            resdf (_type_): _description_
        """
        resdf["Amt_Estimation"] = np.where(resdf["Assumption Type"] == "HVAC Type 2", \
                                  (HVAC_Breakup[resdf["Sub-Technology"]] * buildingArea * resdf["Incentive Value"] * KWH_TO_BTU * HVAC_SO_EUI)/1000000, \
                                  resdf["Incentive Value"])
        return resdf